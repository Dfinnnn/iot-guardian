"""
IoT Guardian — AI-Powered Threat Detection for Smart Healthcare
Entry point / home page. Streamlit auto-loads files in pages/ into the sidebar nav.

This is the empty deploy shell (Task 1). Page content is built in later steps.
"""
import streamlit as st

st.set_page_config(
    page_title="IoT Guardian",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ IoT Guardian")
st.subheader("AI-Powered Threat Detection for Smart Healthcare")

st.markdown(
    """
    Monitoring healthcare IoT (IoMT) network traffic — detecting attacks,
    scoring device risk, and showing the big-data pipeline behind it.

    **This is a deployment shell.** Pages are wired up in later build steps.
    """
)

st.divider()

st.markdown("### Pages")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**1 · Live Threat Monitor**")
    st.caption("Deep Learning — model scores replayed traffic, alerts fire on detection.")
with col2:
    st.markdown("**2 · Device Risk Centre**")
    st.caption("IoT Analytics — per-device risk score, sortable table, quarantine flags.")
with col3:
    st.markdown("**3 · Big Data Pipeline**")
    st.caption("Big Data & Cloud — PySpark preprocessing output, throughput, pipeline diagram.")

st.divider()
st.caption("Academic group project · UMPSA BSD elective · Demo build")
