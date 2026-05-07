"""
Missing data analysis utilities.

This module centralizes functions related to quantifying and
categorizing missing values in tabular epidemiological datasets.

It is designed to support:
- data quality auditing
- temporal stability analysis
- feature selection and preprocessing decisions

The functions in this module are domain-agnostic and can be reused
across different datasets and projects.
"""

import pandas as pd


def calculate_missing_by_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates missing count and percentage per column.

    Returns a DataFrame with:
    - missing_count
    - missing_pct
    """
    if len(df) == 0:
        raise ValueError("DataFrame is empty")

    missing = df.isna().sum().to_frame(name="missing_count")
    missing["missing_pct"] = missing["missing_count"] / len(df) * 100

    return missing.sort_values("missing_pct", ascending=False)


def get_columns_with_missing_pct(
    missing_df: pd.DataFrame,
    pct: float
) -> list[str]:
    """
    Returns column names with missing percentage equal or above pct.
    """
    if "missing_pct" not in missing_df.columns:
        raise ValueError("missing_df must contain a 'missing_pct' column")

    return (
        missing_df[missing_df["missing_pct"] >= pct]
        .index
        .tolist()
    )


def add_missing_ranges(
    missing_df: pd.DataFrame,
    bins: list,
    labels: list
) -> pd.DataFrame:
    """
    Adds a missing_range column using bins and labels.
    """
    if len(labels) != len(bins) - 1:
        raise ValueError("labels must have length len(bins) - 1")

    df = missing_df.copy()
    df["missing_range"] = pd.cut(
        df["missing_pct"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    return df