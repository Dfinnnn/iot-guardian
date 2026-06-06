"""
make_baseline.py  —  run ONCE locally to generate data/baseline.json

Why this exists:
  Page 2's behavioural-anomaly term measures how far each device's frame.time_delta
  sits BELOW the *normal* baseline. That baseline must come from the SAME train split
  Person A used for modelling (Decisions Log B3: "baseline derived from existing train
  split, not a resplit"). We compute it once here and save tiny JSON, so the large
  train.parquet does NOT need to be deployed to Hugging Face — only baseline.json ships.

Usage:
  python make_baseline.py "C:\\path\\to\\eda_outputs\\train.parquet"

Output:
  data/baseline.json
"""
import sys
import json
from pathlib import Path

import pandas as pd

OUT = Path(__file__).parent / "data" / "baseline.json"


def main(train_path: str) -> None:
    df = pd.read_parquet(train_path)

    # Normal traffic only (label == 0) is the reference for "what normal looks like".
    td = pd.to_numeric(df.loc[df["label"] == 0, "frame.time_delta"], errors="coerce").dropna()

    baseline = {
        "source": "train split, normal rows (label==0)",
        "n_normal_rows": int(len(td)),
        # Central tendency of normal inter-packet timing.
        "normal_td_median": float(td.median()),
        # A packet faster than this is "abnormally fast" (flooding signature).
        # 5th percentile of normal => normal traffic rarely trips it, floods trip it heavily.
        "normal_td_p05": float(td.quantile(0.05)),
        "normal_td_p25": float(td.quantile(0.25)),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(baseline, indent=2))
    print("Wrote", OUT)
    print(json.dumps(baseline, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python make_baseline.py "path/to/train.parquet"')
        sys.exit(1)
    main(sys.argv[1])
