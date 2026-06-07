from pathlib import Path
import json
import pandas as pd
import numpy as np
import streamlit as st

# --- Page Setup & Unified Brand Theme ---
st.set_page_config(
    page_title="Device Risk Centre · IoT Guardian", 
    page_icon="🛡️", 
    layout="wide"
)

# Global Injection for App Background Gradient matching the Home Shell
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        180deg,
        #f8fafc 0%,
        #e2e8f0 100%
    );
}
/* Ensure standard expander boxes sit cleanly over custom wrappers */
div[data-testid="stExpander"] { 
    background-color: white !important; 
    border-radius: 15px !important; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    border: none !important;
}
/* Clean up dataframe formatting alignment inside card views */
div[data-testid="stDataFrame"] {
    background-color: white !important;
    padding: 10px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

DATA_DIR = Path(__file__).parent.parent / "data"
TEST_PARQUET = DATA_DIR / "test.parquet"
BASELINE_JSON = DATA_DIR / "baseline.json"

QUARANTINE_THRESHOLD = 40  
NORMAL_WINDOW = 512        
W_STRUCTURAL = 0.6
W_FLOOD = 0.4


# ----------------------------------------------------------------------------- helpers
def _num(series: pd.Series) -> pd.Series:
    """Coerce to numeric, non-numeric -> 0 (synthetic data fills junk with 0/'0')."""
    return pd.to_numeric(series, errors="coerce").fillna(0.0)


@st.cache_data(show_spinner=False)
def load_baseline() -> dict:
    return json.loads(BASELINE_JSON.read_text())


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    return pd.read_parquet(TEST_PARQUET)


@st.cache_data(show_spinner=False)
def compute_device_risk(df: pd.DataFrame, baseline: dict) -> pd.DataFrame:
    td_p05 = baseline["normal_td_p05"]

    work = pd.DataFrame({
        "ip.src": df["ip.src"].astype(str),
        "td": _num(df["frame.time_delta"]),
        "win": _num(df["tcp.window_size_value"]),
        "push": _num(df["tcp.flags.push"]),
        "label": _num(df["label"]),
        "clientid": df["mqtt.clientid"].astype(str),
    })
    
    work["is_fast"] = (work["td"] < td_p05).astype(float)                      
    work["is_malformed"] = ((work["win"] != NORMAL_WINDOW) | (work["push"] != 1)).astype(float)

    g = work.groupby("ip.src")
    dev = pd.DataFrame({
        "packets": g.size(),
        "structural_anomaly": g["is_malformed"].mean() * 100.0,  
        "flood_rate": g["is_fast"].mean() * 100.0,               
        "td_median": g["td"].median(),
        "true_attack_pct": g["label"].mean() * 100.0,            
    })

    dev["risk_score"] = (W_STRUCTURAL * dev["structural_anomaly"] + W_FLOOD * dev["flood_rate"]).clip(0, 100)
    dev["quarantine"] = dev["risk_score"] >= QUARANTINE_THRESHOLD

    def top_clientid(s: pd.Series) -> str:
        vals = s[(s != "0") & (s.str.strip() != "")]
        if len(vals) == 0:
            return "— (synthetic/empty)"
        top = vals.mode()
        return top.iloc[0][:24] if len(top) else "— (synthetic/empty)"

    dev["mqtt.clientid"] = g["clientid"].apply(top_clientid)
    dev = dev.reset_index().sort_values("risk_score", ascending=False).reset_index(drop=True)
    return dev


# --- Error Guard Validation ---
if not TEST_PARQUET.exists() or not BASELINE_JSON.exists():
    st.error(
        "Data not found. Expected `data/test.parquet` and `data/baseline.json`.\n\n"
        "Run locally first:\n"
        "1. Copy `test.parquet` into the `data/` folder.\n"
        "2. `python make_baseline.py \"path/to/train.parquet\"` to generate `data/baseline.json`."
    )
    st.stop()

baseline = load_baseline()
df = load_data()
dev = compute_device_risk(df, baseline)


# ── Home Shell Matched Hero Banner ──────────────────────────────
st.markdown("""
<div style="
background:linear-gradient(90deg,#0f172a,#1e3a8a);
padding:35px;
border-radius:20px;
text-align:center;
color:white;
box-shadow: 0 4px 15px rgba(0,0,0,0.15);
">
<h1>🛡️ IoT Guardian</h1>
<h3>AI-Powered Threat Detection for Smart Healthcare</h3>
<p style="color: #cbd5e1; margin-bottom: 0;">
Deep Learning • Big Data Analytics • Explainable AI — Module 2: Device Risk Centre
</p>
</div>
""", unsafe_allow_html=True)

st.write("") 

# --- Academic Overview Subheader Card ---
st.markdown("""
<div style="background: white; padding: 18px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 20px; text-align: center;">
    <h3 style="margin:0; font-size:18px; color:#1e293b;">IoT Asset Risk Analysis Overview</h3>
</div>
""", unsafe_allow_html=True)

# ── Dynamic System Overview Cards (Home Style Block Matches) ───
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div style="background:#1e293b; padding:20px; border-radius:15px; text-align:center; color:white;">
    <h3 style="font-size:16px; color:#94a3b8; margin:0;">🖥 Total Devices</h3>
    <h1 style="font-size:36px; margin:10px 0 0 0; font-weight:700; font-family:monospace;">{len(dev)}</h1>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background:#991b1b; padding:20px; border-radius:15px; text-align:center; color:white;">
    <h3 style="font-size:16px; color:#fca5a5; margin:0;">🚨 Quarantined</h3>
    <h1 style="font-size:36px; margin:10px 0 0 0; font-weight:700; font-family:monospace;">{int(dev["quarantine"].sum())}</h1>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background:#1e293b; padding:20px; border-radius:15px; text-align:center; color:white;">
    <h3 style="font-size:16px; color:#94a3b8; margin:0;">⚡ Highest Risk</h3>
    <h1 style="font-size:36px; margin:10px 0 0 0; font-weight:700; font-family:monospace;">{dev['risk_score'].max():.0f}</h1>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background:#1e3a8a; padding:20px; border-radius:15px; text-align:center; color:white;">
    <h3 style="font-size:16px; color:#93c5fd; margin:0;">📊 Mean Risk Index</h3>
    <h1 style="font-size:36px; margin:10px 0 0 0; font-weight:700; font-family:monospace;">{dev['risk_score'].mean():.0f}</h1>
    </div>""", unsafe_allow_html=True)

st.write("")

# --- Scoring Logic Container ---
with st.expander("📝 Structural Score Formulation Matrix"):
    st.markdown(
        f"""
        $$\\text{{Risk Score}} = 0.6 \\times \\text{{structural\\_anomaly}} + 0.4 \\times \\text{{flood\\_rate}}$$

        - **Structural Anomaly Coefficient (60% weight)**: Measures the ratio of a given edge asset's incoming packet transfers displaying malformed fields relative to standard architectural protocol constraints ($`tcp.window_size_value` \\neq {NORMAL_WINDOW}$ or $`tcp.flags.push` \\neq 1$). Secure network traffic remains static across these layers; variations register anomalous metrics.
        - **Flood Rate Coefficient (40% weight)**: Identifies the ratio of transmissions falling below the verified normal 5th-percentile inter-packet time delta marker (${baseline['normal_td_p05']:.4g}\\text{{s}}$). This metrics logic serves to segregate high-velocity Denial of Service assets from structural packet variations.

        A device context is flagged as a threat and sent to isolation whenever the computed tracking index vector $\\ge {QUARANTINE_THRESHOLD}$.
        """
    )

st.divider()

# --- Device Risk Table Presentation ---
st.markdown("""
<div style="background: white; padding: 15px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 20px; text-align: center;">
    <h3 style="margin:0; font-size:18px; color:#1e293b;">Central Asset Registry Vector Matrix</h3>
</div>
""", unsafe_allow_html=True)

table = dev.copy()
table["flag"] = table["quarantine"].map({True: "❌ QUARANTINE", False: "✅ OK"})
show = table[[
    "ip.src", "risk_score", "flag", "packets",
    "structural_anomaly", "flood_rate",
    "mqtt.clientid", "true_attack_pct",
]].rename(columns={
    "ip.src": "Device (ip.src)",
    "risk_score": "Risk Score",
    "flag": "Status",
    "packets": "Packets",
    "structural_anomaly": "Structural anomaly %",
    "flood_rate": "Flood rate %",
    "mqtt.clientid": "Client ID (display)",
    "true_attack_pct": "Actual attack % (truth)",
})

st.dataframe(
    show, use_container_width=True, hide_index=True,
    column_config={
        "Risk Score": st.column_config.ProgressColumn(
            "Risk Score", min_value=0, max_value=100, format="%.1f"),
        "Structural anomaly %": st.column_config.NumberColumn(format="%.1f"),
        "Flood rate %": st.column_config.NumberColumn(format="%.1f"),
        "Actual attack % (truth)": st.column_config.NumberColumn(format="%.1f"),
    },
)

st.divider()

# ── Split Section Workspaces (Drill-Down Matrix) ───────────────
st.markdown("""
<div style="background: white; padding: 15px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 20px; text-align: center;">
    <h3 style="margin:0; font-size:18px; color:#1e293b;">🔍 Targeted Network Node Inspection Bus</h3>
</div>
""", unsafe_allow_html=True)

pick = st.selectbox("Select a target device vector from current matrix pool:", dev["ip.src"].tolist())
row = dev[dev["ip.src"] == pick].iloc[0]

# Interactive Device Info Row Styling
st.write("")
d1, d2, d3 = st.columns(3)
with d1:
    status_label = "🚨 QUARANTINE REQUIRED" if row["quarantine"] else "🛡️ ASSET SECURE"
    st.metric("Computed Node Risk Score", f"{row['risk_score']:.1f}", status_label)
with d2:
    st.metric("Aggregated Packets Count", int(row["packets"]))
with d3:
    st.metric("Actual Attack Ground-Truth Ratio", f"{row['true_attack_pct']:.1f}%")

# Drilldown Layout Structure split 50/50
left_chart, right_table = st.columns([1, 1], gap="large")

with left_chart:
    st.markdown("<p style='font-weight:600; font-size:14px; color:#1e293b; margin-bottom:8px;'>Visual Contribution Weight Distribution Matrix</p>", unsafe_allow_html=True)
    contrib = pd.DataFrame({
        "Term": ["Structural Anomaly Score Component (x0.6)", "Flood Velocity Ratio Component (x0.4)"],
        "Weighted points": [W_STRUCTURAL * row["structural_anomaly"], W_FLOOD * row["flood_rate"]],
    })
    st.bar_chart(contrib.set_index("Term")["Weighted points"], use_container_width=True)

with right_table:
    st.markdown("<p style='font-weight:600; font-size:14px; color:#1e293b; margin-bottom:8px;'>Tabular Verification Breakdown</p>", unsafe_allow_html=True)
    full_contrib = pd.DataFrame({
        "Mathematical Score Term": ["Structural Anomaly (x0.6)", "Flood Rate (x0.4)"],
        "Raw Observed Percentage": [row["structural_anomaly"], row["flood_rate"]],
        "Aggregated Point Values": [W_STRUCTURAL * row["structural_anomaly"], W_FLOOD * row["flood_rate"]],
    })
    st.dataframe(
        full_contrib.style.format({"Raw Observed Percentage": "{:.1f}%", "Aggregated Point Values": "{:.2f}"}),
        use_container_width=True, hide_index=True,
    )

st.markdown(f"""
<div style="background: #e0e7ff; color: #1e3a8a; padding: 15px; border-radius: 12px; font-size: 13px; font-family: monospace; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-top:15px;">
    ℹ️ <b>Node Profile Metadata:</b> Median observed frame time gap is <b>{row['td_median']:.4g}s</b> 
    (Normal baseline criteria tracking median sits at {baseline['normal_td_median']:.4g}s). 
    Identified payload string variant: <code>{row['mqtt.clientid']}</code>.
</div>
""", unsafe_allow_html=True)

# Footer Standard Template Module Match
st.markdown("""
<div style="text-align:center; padding:40px 0 20px 0; color:gray; font-size:12px;">
BSD Elective Project • IoT Guardian • UMPSA Data Analytics
</div>
""", unsafe_allow_html=True)