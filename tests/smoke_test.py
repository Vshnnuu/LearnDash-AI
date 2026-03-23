from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from configs.settings import DATA_PATH, FEATURE_COLS, TARGET_COL


def main():
    assert Path(DATA_PATH).exists(), f"Missing dataset: {DATA_PATH}"
    df = pd.read_csv(DATA_PATH)
    assert not df.empty, "Dataset is empty"
    assert TARGET_COL in df.columns, "Target column missing"
    for col in FEATURE_COLS:
        assert col in df.columns, f"Missing feature column: {col}"
    print("Smoke test passed.")


if __name__ == "__main__":
    main()
