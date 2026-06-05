"""
Page 2 — Device Risk Centre
Elective: IoT Analytics
Build basis: pure-Pandas risk score (0-100), sortable device table,
quarantine flags for high-risk devices, per-device drill-down.

Risk score (B3, Decisions Log):
  (attack_count * 0.4) + (behavioural_anomaly * 0.4) + (protocol_risk_weight * 0.2)
  - behavioural_anomaly = pure-Pandas frame.time_delta deviation vs train-split
    normal baseline (NOT model-derived).
  - device key = ip.src; mqtt.clientid shown as display attribute only.

STUB — built next (Task 2).
"""
import streamlit as st

st.set_page_config(page_title="Device Risk Centre · IoT Guardian", page_icon="🛡️", layout="wide")

st.title("2 · Device Risk Centre")
st.caption("IoT Analytics elective")

st.info("Coming soon — per-device risk scoring, sortable table, and quarantine flags.")
