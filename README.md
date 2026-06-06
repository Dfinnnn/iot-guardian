---
title: IoT Guardian
emoji: 🛡️
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.58.0
app_file: app.py
pinned: false
---

# IoT Guardian — AI-Powered Threat Detection for Smart Healthcare

Academic group research project (UMPSA, BSD elective). Monitors healthcare IoT (IoMT)
network traffic: detects attacks (Deep Learning), scores device risk (IoT Analytics),
and shows the big-data preprocessing pipeline (Big Data & Cloud Computing).

## Pages
1. **Live Threat Monitor** — model scores replayed traffic; alerts fire on detection.
2. **Device Risk Centre** — per-device risk score, sortable table, quarantine flags.
3. **Big Data Pipeline** — PySpark preprocessing output, throughput, pipeline diagram.

> Deploy shell. Page content is wired up in later build steps.

## Run locally
```bash
pip install -r requirements.txt

# one-time data setup (Page 2):
#   1. copy your EDA test.parquet into data/
#   2. generate the normal baseline from train.parquet:
python make_baseline.py "path/to/eda_outputs/train.parquet"

streamlit run app.py
```
