"""
DataFrame column manipulation helpers.

This module contains lightweight utility functions to safely
manipulate and inspect DataFrame schemas, avoiding errors due
to missing or inconsistent column presence across datasets.
"""

import pandas as pd
from typing import Iterable, Set


def drop_columns_safe(
    df: pd.DataFrame,
    columns: list[str],
    verbose: bool = False
) -> pd.DataFrame:
    """
    Drops columns only if they exist in the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    columns : list[str]
        List of columns to drop.
    verbose : bool, optional
        Whether to print how many columns were dropped.

    Returns
    -------
    pd.DataFrame
        DataFrame without the specified columns.
    """
    existing = [c for c in columns if c in df.columns]

    if verbose:
        print(f"Dropped {len(existing)} columns")

    return df.drop(columns=existing)


def inspect_column_values(
    df: pd.DataFrame,
    columns: Iterable[str],
    max_values: int = 10
) -> pd.DataFrame:
    """
    Inspects unique non-null values for selected columns.

    Useful for exploratory analysis and data auditing.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    columns : iterable of str
        Columns to inspect.
    max_values : int, optional
        Maximum number of unique values to display per column.

    Returns
    -------
    pd.DataFrame
        Table with number of unique values and a sample of them.
    """
    records = []

    for col in columns:
        if col not in df.columns:
            continue

        values = (
            df[col]
            .dropna()
            .unique()
            .tolist()
        )

        records.append({
            "column": col,
            "n_unique": len(values),
            "unique_values": values[:max_values]
        })

    return (
        pd.DataFrame(records)
        .sort_values("n_unique", ascending=False)
        .reset_index(drop=True)
    )


def check_binary_pattern(
    df: pd.DataFrame,
    columns: Iterable[str],
    expected_values: Set = {1, 2}
) -> pd.DataFrame:
    """
    Checks whether columns follow a binary / categorical pattern.

    By default, verifies adherence to the {1, 2} pattern
    commonly used in epidemiological forms.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    columns : iterable of str
        Columns to inspect.
    expected_values : set, optional
        Set of expected valid values (default: {1, 2}).

    Returns
    -------
    pd.DataFrame
        Table with detected unique values and classification status:
        - OK: only expected values
        - MIXED: expected + unexpected values
        - NON_STANDARD: only unexpected values
        - EMPTY: column has no non-null values
    """
    records = []

    for col in columns:
        if col not in df.columns:
            continue

        values = set(
            df[col]
            .dropna()
            .unique()
            .tolist()
        )

        if not values:
            status = "EMPTY"
        elif values.issubset(expected_values):
            status = "OK"
        elif values.intersection(expected_values):
            status = "MIXED"
        else:
            status = "NON_STANDARD"

        records.append({
            "column": col,
            "unique_values": sorted(values),
            "status": status
        })

    return (
        pd.DataFrame(records)
        .sort_values("status")
        .reset_index(drop=True)
    )