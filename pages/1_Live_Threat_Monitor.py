import pickle
import time
import numpy as np
import pandas as pd
import streamlit as st
from tensorflow.keras.models import load_model

# --- Page Setup & Unified Brand Theme ---
st.set_page_config(
    page_title="Live Threat Monitor · IoT Guardian",
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
</style>
""", unsafe_allow_html=True)

DATA_PATH   = "data/demo_stream.csv"
MODEL_DIR   = "models"
THRESHOLD   = 0.50
SEED        = 42

# ── Locked feature order — must match training exactly ──────────
NUMERIC_FEATURES = [
    'tcp.window_size_value', 'frame.len', 'tcp.pdu.size', 'tcp.ack',
    'tcp.hdr_len', 'tcp.time_delta', 'mqtt.msgtype', 'frame.time_delta',
    'tcp.flags.push', 'tcp.dstport', 'ip.ttl', 'mqtt.qos',
    'tcp.flags.ack', 'mqtt.dupflag', 'tcp.connection.syn', 'tcp.flags.syn',
]
CATEGORICAL_FEATURES = [
    'tcp.flags', 'mqtt.conack.flags', 'mqtt.conflags', 'mqtt.hdrflags',
]
ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES 


# ── Model loading (once per app start) ─────────────────────────
@st.cache_resource
def load_artifacts():
    mlp_model = load_model(f"{MODEL_DIR}/mlp_model.keras")
    with open(f"{MODEL_DIR}/robust_scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open(f"{MODEL_DIR}/freq_encoders.pkl", "rb") as f:
        freq_enc = pickle.load(f)
    with open(f"{MODEL_DIR}/shap_cache.pkl", "rb") as f:
        shap_cache = pickle.load(f)
    return mlp_model, scaler, freq_enc, shap_cache


@st.cache_data
def load_stream():
    return pd.read_csv(DATA_PATH)


# ── Real scorer ─────────────────────────────────────────────────
def real_score(row, mlp_model, scaler, freq_enc):
    d = {}
    for col in NUMERIC_FEATURES:
        val = row[col]
        d[col] = float(val) if pd.notna(val) else 0.0

    for col in CATEGORICAL_FEATURES:
        raw_val = str(row[col])
        d[col] = freq_enc[col].get(raw_val, 0.0)

    X = np.array([[d[col] for col in ALL_FEATURES]], dtype=np.float32)
    X_scaled = scaler.transform(X)
    prob = float(mlp_model.predict(X_scaled, verbose=0)[0][0])
    return prob


def get_top_features(shap_cache, k=3):
    top_df = shap_cache["feature_importance"].head(k)
    return list(zip(top_df["feature"], top_df["importance"]))


# ── Matched High-Contrast Security Alert Card ───────────────────
def render_alert(slot, alert):
    score = alert["score"]
    if score >= 0.95:
        severity, color_hex = "Critical", "#991b1b"
    elif score >= 0.80:
        severity, color_hex = "High", "#ea580c"
    else:
        severity, color_hex = "Medium", "#eab308"

    with slot.container():
        st.markdown(f"""
        <div style="
            background: #ffffff;
            padding: 24px;
            border-radius: 15px;
            border-left: 6px solid {color_hex};
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 16px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <h4 style="margin: 0; color: {color_hex}; font-size: 16px;">🚨 SECURITY THREAT RECORDED</h4>
                <span style="font-family: monospace; font-size: 13px; color: #64748b; font-weight: 600;">Packet #{alert['idx']}</span>
            </div>
            <div style="display: flex; gap: 40px; margin-bottom: 12px;">
                <div>
                    <p style="margin:0; font-size:12px; color:#64748b; text-transform:uppercase; font-weight:600;">Source Device</p>
                    <p style="margin:4px 0 0 0; color:#1e293b; font-family:monospace; font-size:17px; font-weight:700;">{alert['ip']}</p>
                </div>
                <div>
                    <p style="margin:0; font-size:12px; color:#64748b; text-transform:uppercase; font-weight:600;">Threat Score</p>
                    <p style="margin:4px 0 0 0; color:#1e293b; font-family:monospace; font-size:17px; font-weight:700;">{score:.2f}</p>
                </div>
                <div>
                    <p style="margin:0; font-size:12px; color:#64748b; text-transform:uppercase; font-weight:600;">Severity Level</p>
                    <p style="margin:4px 0 0 0; color:{color_hex}; font-size:17px; font-weight:700;">{severity}</p>
                </div>
            </div>
            <div style="background: #f8fafc; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0;">
                <p style="margin:0 0 6px 0; font-size:11px; color:#64748b; text-transform:uppercase; font-weight:600; letter-spacing:0.5px;">🧠 Key Threat Indicators (SHAP Attribution)</p>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                    {" ".join([f"<span style='background:white; border:1px solid #cbd5e1; padding:2px 8px; border-radius:4px; font-size:12px; font-family:monospace;'><b>{f}</b> ({v:+.3f})</span>" for f, v in alert["top"]])}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── Load artifacts + data ───────────────────────────────────────
mlp_model, scaler, freq_enc, shap_cache = load_artifacts()
df = load_stream()

if "alerts" not in st.session_state:
    st.session_state.alerts = []

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
Deep Learning • Big Data Analytics • Explainable AI — Module 1: Live Threat Monitor
</p>
</div>
""", unsafe_allow_html=True)

st.write("") 

with st.expander("How this page works"):
    st.markdown(
        f"""
        Replays `{DATA_PATH}` ({len(df)} packets) row-by-row as a simulated live feed
        (`st.empty()` + `time.sleep()` — not real WebSockets). Each packet is scored
        by the deployed **MLP Neural Network** model (F1 = 0.9997 on test set); an alert card
        fires and **accumulates** when score $\\ge {THRESHOLD:.2f}$.

        **Model selection:** RF was chosen over MLP (F1 = 0.9997) and GRU
        (F1 = 0.9181) via a three-way comparison — simpler, faster, and SHAP-compatible.
        GRU's lower score confirms sequence architectures add nothing on shuffled
        per-packet tabular data.
        """
    )

# ── Control Interface Box ───────────────────────────────────────
st.markdown("""
<div style="background: white; padding: 15px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); text-align: center; margin-bottom: 18px;">
    <h4 style="margin:0; color:#1e293b; font-size:16px;">System Replay Execution Panel</h4>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 2])
start = c1.button("▶ Start replay", use_container_width=True, type="primary")
if c2.button("⟲ Reset", use_container_width=True):
    st.session_state.alerts = []
    st.rerun()
speed = c3.select_slider("Replay speed (sec / packet)", options=[0.05, 0.1, 0.2, 0.3, 0.5], value=0.2)

st.write("")

# ── System Dashboard Metric Headers ─────────────────────────────
st.markdown("""
<div style="background: white; padding: 15px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 20px; text-align: center;">
    <h3 style="margin:0; font-size:18px; color:#1e293b;">Live Metric KPI Overview</h3>
</div>
""", unsafe_allow_html=True)

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
kpi1_slot = kpi_col1.empty()
kpi2_slot = kpi_col2.empty()
kpi3_slot = kpi_col3.empty()

# Baseline layout macro function to inject real-time updates inside Home style cards
def draw_kpi_cards(p_count=0, t_count=0, d_rate="0.0%"):
    kpi1_slot.markdown(f"""
    <div style="background: #1e293b; padding: 20px; border-radius: 15px; text-align: center; color: white;">
    <h3 style="font-size:16px; color:#94a3b8; margin:0;">📦 Packets Analysed</h3>
    <h1 style="font-size:36px; margin:10px 0 0 0; font-weight:700; font-family:monospace;">{p_count}</h1>
    </div>""", unsafe_allow_html=True)
    
    kpi2_slot.markdown(f"""
    <div style="background: #991b1b; padding: 20px; border-radius: 15px; text-align: center; color: white;">
    <h3 style="font-size:16px; color:#fca5a5; margin:0;">🚨 Threats Detected</h3>
    <h1 style="font-size:36px; margin:10px 0 0 0; font-weight:700; font-family:monospace;">{t_count}</h1>
    </div>""", unsafe_allow_html=True)
    
    kpi3_slot.markdown(f"""
    <div style="background: #1e3a8a; padding: 20px; border-radius: 15px; text-align: center; color: white;">
    <h3 style="font-size:16px; color:#93c5fd; margin:0;">🧠 Detection Rate</h3>
    <h1 style="font-size:36px; margin:10px 0 0 0; font-weight:700; font-family:monospace;">{d_rate}</h1>
    </div>""", unsafe_allow_html=True)

# Draw initial 0 values
draw_kpi_cards()

st.divider()

# ── Workspace Layout ────────────────────────────────────────────
left, right = st.columns([1.1, 1.9], gap="large")
with left:
    st.markdown("""
    <div style="background: white; padding: 12px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); text-align: center; margin-bottom: 16px;">
        <h4 style="margin:0; color:#1e293b;">📊 Telemetry Feed</h4>
    </div>
    """, unsafe_allow_html=True)
    status_slot = st.empty()
    gauge_slot  = st.empty()
    progress    = st.empty()
    
    status_slot.markdown("""
    <div style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center; border: 1px dashed #cbd5e1;">
        <p style="margin: 0; color: #94a3b8; font-family: monospace;">Awaiting pipeline initialization...</p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div style="background: white; padding: 12px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); text-align: center; margin-bottom: 16px;">
        <h4 style="margin:0; color:#1e293b;">⚡ Real-time Threat Alarms</h4>
    </div>
    """, unsafe_allow_html=True)
    alert_feed = st.container()

for a in reversed(st.session_state.alerts):
    render_alert(alert_feed.empty(), a)


# ── Replay loop ─────────────────────────────────────────────────
if start:
    st.session_state.alerts = []
    total = len(df)

    for i, row in df.iterrows():
        score = real_score(row, mlp_model, scaler, freq_enc)
        is_attack = score >= THRESHOLD

        processed_packets = i + 1
        attack_count = len(st.session_state.alerts)
        rate = (attack_count / processed_packets * 100 if processed_packets > 0 else 0)

        # Dynamic KPI Update via Home Screen Component Styles
        draw_kpi_cards(
            p_count=processed_packets, 
            t_count=attack_count, 
            d_rate=f"{rate:.1f}%"
        )

        # High-Contrast Terminal Output Card matching layout properties
        status_slot.markdown(f"""
        <div style="
            background: #1e293b; 
            color: #f8fafc; 
            padding: 24px; 
            border-radius: 15px; 
            font-family: monospace;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        ">
            <div style="display: flex; justify-content: space-between; margin-bottom: 14px; border-bottom: 1px solid #475569; padding-bottom: 8px;">
                <span style="color: #facc15; font-weight: bold;">📦 FRAME MONITOR</span>
                <span style="color: #94a3b8;">{i+1} / {total}</span>
            </div>
            <p style="margin: 6px 0; font-size: 13px;"><span style="color: #94a3b8;">SOURCE LAYER IP :</span> {row['ip.src']}</p>
            <p style="margin: 6px 0; font-size: 13px;"><span style="color: #94a3b8;">TARGET DEST IP :</span> {row['ip.dst']}</p>
            <div style="margin-top: 20px; display: flex; justify-content: space-between; align-items: center;">
                <span style="
                    background: {'#991b1b' if is_attack else '#1e3a8a'};
                    color: white;
                    padding: 4px 12px;
                    border-radius: 6px;
                    font-size: 12px;
                    font-weight: bold;
                ">
                    {"🔴 THREAT DETECTED" if is_attack else "🟢 NORMAL TRAFFIC"}
                </span>
                <span style="font-size: 18px; font-weight: 700; color: white;">Prob: {score:.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        gauge_slot.progress(score, text=f"threat score {score:.2f}")
        progress.caption(f"replaying… {i+1}/{total}")

        if is_attack:
            alert = {
                "idx":   int(i + 1),
                "ip":    str(row["ip.src"]),
                "score": score,
                "top":   get_top_features(shap_cache),
            }
            st.session_state.alerts.append(alert)
            # Fresh update of the stats after append to keep metrics lock-step
            draw_kpi_cards(
                p_count=processed_packets, 
                t_count=len(st.session_state.alerts), 
                d_rate=f"{(len(st.session_state.alerts) / processed_packets * 100):.1f}%"
            )
            render_alert(alert_feed.empty(), alert)

        time.sleep(speed)

    progress.markdown(f"""
    <div style="background: #e0e7ff; color: #1e3a8a; padding: 15px; border-radius: 12px; font-size: 14px; font-weight: 600; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        🎉 Evaluation pipeline complete. Recorded {len(st.session_state.alerts)} total threat vectors across {total} evaluated network frames.
    </div>
    """, unsafe_allow_html=True)