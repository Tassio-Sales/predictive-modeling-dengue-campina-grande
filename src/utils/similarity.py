"""
Column similarity utilities.

This module provides structure-level analysis of column names,
with the goal of identifying suspected duplicated or legacy columns
across heterogeneous datasets.

Similarity is computed after column name normalization and is based
solely on lexical resemblance, not semantic or clinical meaning.

This module is intended to support:
- schema consolidation across years
- detection of redundant variables
- dataset cleaning and auditing

It should NOT be used for clinical or semantic interpretation.
"""

from difflib import SequenceMatcher
from itertools import combinations
import pandas as pd
from utils.name_normalizer import normalize_column_name

def column_name_similarity(a: str, b: str) -> float:
    a_norm = normalize_column_name(a)
    b_norm = normalize_column_name(b)
    return SequenceMatcher(None, a_norm, b_norm).ratio()


def find_suspected_duplicate_columns(
    
    df: pd.DataFrame,
    missing_df: pd.DataFrame,
    similarity_threshold: float = 0.75,
    missing_threshold: float = 95
) -> pd.DataFrame:
    """
    Identify pairs of columns that are likely duplicates.

    Two columns are considered suspected duplicates if:
    - their normalized names exceed a similarity threshold
    - at least one of them presents a high missing rate,
      suggesting partial or temporal usage

    This function operates at the schema level and does not
    evaluate semantic or clinical equivalence.
    """
    if "missing_pct" not in missing_df.columns:
        raise ValueError("missing_df must contain a 'missing_pct' column")

    suspects = []

    for col1, col2 in combinations(df.columns, 2):

        if col1 not in missing_df.index or col2 not in missing_df.index:
            continue

        sim = column_name_similarity(col1, col2)

        if sim < similarity_threshold:
            continue

        miss1 = missing_df.loc[col1, "missing_pct"]
        miss2 = missing_df.loc[col2, "missing_pct"]

        if miss1 >= missing_threshold or miss2 >= missing_threshold:
            suspects.append({
                "column_1": col1,
                "column_2": col2,
                "similarity": round(sim, 3),
                "missing_pct_1": round(miss1, 2),
                "missing_pct_2": round(miss2, 2),
            })

    if not suspects:
        return pd.DataFrame(
            columns=[
                "column_1",
                "column_2",
                "similarity",
                "missing_pct_1",
                "missing_pct_2",
            ]
        )

    return (
        pd.DataFrame(suspects)
        .sort_values(
            ["similarity", "missing_pct_1", "missing_pct_2"],
            ascending=False
        )
    )