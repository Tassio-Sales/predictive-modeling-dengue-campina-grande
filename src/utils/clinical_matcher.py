"""
Clinical column matcher.

Identifies clinical variables using:
- normalized column names
- semantic tokens
- domain vocabularies
- prefix-based clinical rules
- missing data penalties
"""
from difflib import SequenceMatcher
import pandas as pd

from utils.name_normalizer import normalize_column_name
from utils.clinical_vocab import (
    SYMPTOMS,
    ALARM_SIGNS,
    SEVERITY_SIGNS,
    COMORBIDITIES,
)

# Columns that are clearly administrative, laboratory results or IDs
FORBIDDEN_PREFIXES = (
    "DT_",
    "ID_",
)

FORBIDDEN_TOKENS = {
    "ID",
    "RESUL",
    "RESULT",
    "NS1",
    "PCR",
    "PRNT",
    "SORO",
    "VI",
    "REGION",
    "AGRAVO",
    "BAINF",
    "FHD",
}


def similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def infer_group_by_prefix(column_name: str) -> str | None:
    """
    Enforces SINAN clinical hierarchy using column prefixes.
    """
    col = column_name.upper()
    if col.startswith("GRAV_"):
        return "SEVERITY"
    if col.startswith("ALRM_"):
        return "ALARM"
    return None


def contains_forbidden_token(tokens: list[str]) -> bool:
    tokens_upper = {t.upper() for t in tokens}
    return bool(tokens_upper & FORBIDDEN_TOKENS)


def best_vocab_match(texts: list[str], vocab: dict) -> tuple[str | None, float]:
    """
    Returns best matching concept using token-level similarity.
    """
    best_concept = None
    best_score = 0.0

    for concept, variants in vocab.items():
        for variant in variants:
            v = variant.lower()

            for text in texts:
                for token in text.split("_"):
                    score = similarity(token, v)
                    if score > best_score:
                        best_score = score
                        best_concept = concept

    return best_concept, best_score


def match_clinical_columns(
    df: pd.DataFrame,
    missing_by_col: pd.DataFrame,
    similarity_threshold: float = 0.6,
) -> pd.DataFrame:
    """
    Matches dataset columns to clinical concepts.

    Returns a DataFrame with:
    - column
    - normalized_name
    - group    
    - similarity_score
    - missing_pct
    """

    records = []

    for col in df.columns:

        col_upper = col.upper()

        # Hard block by prefix
        if col_upper.startswith(FORBIDDEN_PREFIXES):
            continue

        norm = normalize_column_name(col)

        base_name = norm.get("base_name", "")
        semantic_tokens = norm.get("semantic_tokens", [])

        # Block administrative / lab columns by tokens
        if contains_forbidden_token(semantic_tokens):
            continue

        texts_to_compare = [
            base_name.lower(),
            col.lower(),
            *[t.lower() for t in semantic_tokens],
        ]

        try:
            missing_pct = float(missing_by_col.loc[col, "missing_pct"])
        except Exception:
            missing_pct = 0.0

        forced_group = infer_group_by_prefix(col)

        for group_name, vocab in [
            ("SYMPTOM", SYMPTOMS),
            ("ALARM", ALARM_SIGNS),
            ("SEVERITY", SEVERITY_SIGNS),
            ("COMORBIDITY", COMORBIDITIES),
        ]:
            # Respect SINAN hierarchy
            if forced_group and group_name != forced_group:
                continue

            concept, score = best_vocab_match(texts_to_compare, vocab)

            if not concept or score < similarity_threshold:
                continue

            records.append({
                "column": col,
                "normalized_name": base_name,
                "group": group_name,                
                "similarity_score": round(score, 3),
                "missing_pct": round(missing_pct, 2),
            })

    if not records:
        return pd.DataFrame(
            columns=[
                "column",
                "normalized_name",
                "group",                
                "similarity_score",
                "missing_pct",
            ]
        )

    return (
        pd.DataFrame(records)
        .sort_values(
            ["group", "column", "similarity_score"],
            ascending=[True, True, False]
        )
        .reset_index(drop=True)
    )

def resolve_group_conflicts(df_matches: pd.DataFrame) -> pd.DataFrame:
    """
    Resolves cases where the same column is matched to multiple clinical groups.
    Ensures exactly ONE final group per column using deterministic clinical rules.
    """

    GROUP_PRIORITY = {
        "SEVERITY": 3,
        "ALARM": 2,
        "SYMPTOM": 1,
        "COMORBIDITY": 0,
    }

    COMORBIDITY_KEYWORDS = (
        "RENAL",
        "DIABET",
        "AUTO",
        "HEPAT",
        "HEMATO",
        "HIPERT",
        "CARDIO",
        "PULMON",
        "NEURO",
        "IMUNO",
    )

    SYMPTOM_KEYWORDS = (
        "DOR",
        "FEBRE",
        "CEFA",
        "MIAL",
        "ARTR",
        "NAUSE",
        "VOM",
        "EXANT",
        "PETE",
        "CONJUNT",
        "LEUCO",
    )

    resolved_rows = []

    for column, df_col in df_matches.groupby("column"):

        if df_col["group"].nunique() == 1:
            resolved_rows.append(df_col.iloc[0])
            continue

        column_upper = column.upper()
        normalized_name = df_col.iloc[0]["normalized_name"].upper()
        
        if column_upper.startswith("GRAV_"):
            row = df_col[df_col["group"] == "SEVERITY"]
            if not row.empty:
                resolved_rows.append(row.iloc[0])
                continue

        if column_upper.startswith("ALRM_"):
            row = df_col[df_col["group"] == "ALARM"]
            if not row.empty:
                resolved_rows.append(row.iloc[0])
                continue
        
        if any(k in column_upper or k in normalized_name for k in COMORBIDITY_KEYWORDS):
            row = df_col[df_col["group"] == "COMORBIDITY"]
            if not row.empty:
                resolved_rows.append(row.iloc[0])
                continue
        
        if any(k in column_upper or k in normalized_name for k in SYMPTOM_KEYWORDS):
            row = df_col[df_col["group"] == "SYMPTOM"]
            if not row.empty:
                resolved_rows.append(row.iloc[0])
                continue
        
        df_tmp = df_col.copy()
        df_tmp["group_priority"] = df_tmp["group"].map(GROUP_PRIORITY)

        resolved_rows.append(
            df_tmp
            .sort_values(
                ["group_priority", "similarity_score"],
                ascending=[False, False]
            )
            .iloc[0]
        )

    return (
        pd.DataFrame(resolved_rows)
        .drop(columns=["group_priority"], errors="ignore")
        .reset_index(drop=True)
    )
