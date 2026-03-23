from __future__ import annotations

import pandas as pd
from configs.settings import DATA_PATH, TARGET_COL, ID_COLS, FEATURE_COLS


def load_dataset(path=DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def validate_dataset(df: pd.DataFrame) -> None:
    required_cols = set(FEATURE_COLS + [TARGET_COL] + ID_COLS)
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    if df.isna().sum().sum() > 0:
        raise ValueError("Dataset contains missing values. Clean or impute before training.")

    if df.duplicated().sum() > 0:
        raise ValueError("Dataset contains duplicate rows. Remove them before training.")

    unique_targets = set(df[TARGET_COL].unique().tolist())
    if not unique_targets.issubset({0, 1}):
        raise ValueError(f"Target column must be binary 0/1. Found: {sorted(unique_targets)}")


def get_X_y(df: pd.DataFrame):
    X = df[FEATURE_COLS].copy()
    y = df[TARGET_COL].copy()
    return X, y
