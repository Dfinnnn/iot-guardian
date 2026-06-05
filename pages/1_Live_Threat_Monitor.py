"""
Page 1 — Live Threat Monitor
Elective: Deep Learning
Build basis: replays CSV as a live feed; RF model scores each packet;
alert cards fire on detection (cached SHAP on sample alerts).

STUB — built in a later step (Person B UI, Person A wires the model).
"""
import streamlit as st

st.set_page_config(page_title="Live Threat Monitor · IoT Guardian", page_icon="🛡️", layout="wide")

st.title("1 · Live Threat Monitor")
st.caption("Deep Learning elective")

st.info("Coming soon — this page will replay traffic and fire model-based threat alerts.")
