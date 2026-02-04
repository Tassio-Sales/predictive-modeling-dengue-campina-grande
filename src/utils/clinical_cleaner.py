"""
Clinical post-processing cleaner.

Applies rule-based clinical corrections AFTER automatic matching:
- removes known false positives
- fixes known group misclassifications
"""

import pandas as pd

FALSE_POSITIVE_COLUMNS = {
    "HISTOPA_N",    
    "TPAUTOCTO", 
}



FORCED_GROUP_OVERRIDES = {
    "ACIDO_PEPT": "COMORBIDITY", 
}


def clean_clinical_matches(df_matches: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans clinical matching output using domain knowledge.

    Steps:
    1. Remove known false positives
    2. Apply forced group corrections
    """

    df = df_matches.copy()
    
    df = df[~df["column"].isin(FALSE_POSITIVE_COLUMNS)]
 
    df["group"] = df.apply(
        lambda row: FORCED_GROUP_OVERRIDES.get(row["column"], row["group"]),
        axis=1
    )

    return df.reset_index(drop=True)

def group_clinical_duplicates(
    df_matches: pd.DataFrame,
) -> pd.DataFrame:
    """
    Identifies potential duplicated clinical columns
    based on:
    - same clinical group
    - same canonical normalized_name (handles plural forms)

    Returns only duplicated columns with a duplicate_group label.
    """

    df = df_matches.copy()

    # Canonical form for duplication detection
    def canonical_name(name: str) -> str:
        name = name.lower()
        if name.endswith("s") and len(name) > 4:
            return name[:-1]
        return name

    df["canonical_name"] = df["normalized_name"].apply(canonical_name)

    # Duplication key
    df["dup_key"] = (
        df["group"].str.upper() + "__" +
        df["canonical_name"]
    )

    # Count duplicates
    dup_counts = (
        df.groupby("dup_key")["column"]
        .transform("count")
    )

    df = df[dup_counts > 1].copy()

    df["duplicate_group"] = df["canonical_name"]

    return (
        df.sort_values(
            ["group", "duplicate_group", "missing_pct"],
            ascending=[True, True, True]
        )
        .reset_index(drop=True)
    )

def resolve_duplicate_columns(df_matches: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Resolve duplicated clinical columns based on missing percentage.

    Rule:
    - For each dup_key, keep the column with the lowest missing_pct
    - Mark others for removal

    Returns:
    - df_kept: columns to keep
    - df_removed: columns to remove (with reason)
    """

    kept_records = []
    removed_records = []

    for dup_key, group_df in df_matches.groupby("dup_key"):

        # Sort by missing percentage (ascending)
        group_df = group_df.sort_values("missing_pct")

        # Best column = least missing
        best_row = group_df.iloc[0]
        kept_records.append(best_row)

        # Remaining are duplicates to remove
        for _, row in group_df.iloc[1:].iterrows():
            removed_records.append({
                **row.to_dict(),
                "kept_column": best_row["column"],
                "kept_missing_pct": best_row["missing_pct"],
                "removal_reason": "higher_missing_pct"
            })

    df_kept = pd.DataFrame(kept_records).reset_index(drop=True)
    df_removed = pd.DataFrame(removed_records).reset_index(drop=True)

    return df_kept, df_removed