import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup & Unified Brand Theme ---
st.set_page_config(
    page_title="Big Data Pipeline · IoT Guardian",
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
/* Ensure tab components rest cleanly above the background wrapper gradient */
div[data-testid="stTabs"] {
    background-color: transparent !important;
}
div[data-baseweb="tab-panel"] {
    background: white !important;
    padding: 25px;
    border-radius: 0 0 15px 15px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important;
}
div[data-baseweb="tab-list"] {
    background: #1e293b !important;
    border-radius: 15px 15px 0 0 !important;
    padding: 6px 12px 0 12px !important;
}
button[data-baseweb="tab"] {
    color: #cbd5e1 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #facc15 !important;
    border-bottom-color: #facc15 !important;
}
div[data-testid="stDataFrame"] {
    background-color: white !important;
    padding: 5px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ── Home Shell Matched Hero Banner ──────────────────────────────
st.markdown("""
<div style="
background: linear-gradient(90deg, #0f172a, #1e3a8a);
padding: 35px;
border-radius: 20px;
text-align: center;
color: white;
box-shadow: 0 4px 15px rgba(0,0,0,0.15);
">
<h1>🛡️ IoT Guardian</h1>
<h3>AI-Powered Threat Detection for Smart Healthcare</h3>
<p style="color: #cbd5e1; margin-bottom: 0;">
Deep Learning • Big Data Analytics • Explainable AI — Module 3: Big Data Threat Intelligence Center
</p>
</div>
""", unsafe_allow_html=True)

st.write("") 


# ==========================
# LOAD DATA
# ==========================
device_risk = pd.read_csv("outputs/device_risk.csv")
topic_stats = pd.read_csv("outputs/topic_stats.csv")
msgtype_stats = pd.read_csv("outputs/msgtype_stats.csv")


# --- Main Navigation Operational Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Pipeline Overview",
    "🖥 Device Risk Analytics",
    "📡 MQTT Protocol Intelligence",
    "🚨 Core Threat Insights"
])


# ==========================================
# TAB 1: OVERVIEW & PIPELINE FLOW
# ==========================================
with tab1:
    st.markdown("<h4 style='color:#1e293b; margin-top:0;'>📊 PySpark Central Data Aggregations</h4>", unsafe_allow_html=True)

    # Dynamic KPI Overview Blocks matching core metric templates
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div style="background:#1e293b; padding:20px; border-radius:15px; text-align:center; color:white;">
        <h3 style="font-size:14px; color:#94a3b8; margin:0; text-transform:uppercase;">📦 Total Records</h3>
        <h1 style="font-size:32px; margin:10px 0 0 0; font-weight:700; font-family:monospace;">132,085</h1>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#14532d; padding:20px; border-radius:15px; text-align:center; color:white;">
        <h3 style="font-size:14px; color:#a3e635; margin:0; text-transform:uppercase;">✅ Normal Traffic</h3>
        <h1 style="font-size:32px; margin:10px 0 0 0; font-weight:700; font-family:monospace;">75,997</h1>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background:#991b1b; padding:20px; border-radius:15px; text-align:center; color:white;">
        <h3 style="font-size:14px; color:#fca5a5; margin:0; text-transform:uppercase;">🚨 Attack Traffic</h3>
        <h1 style="font-size:32px; margin:10px 0 0 0; font-weight:700; font-family:monospace;">56,088</h1>
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div style="background:#1e3a8a; padding:20px; border-radius:15px; text-align:center; color:white;">
        <h3 style="font-size:14px; color:#93c5fd; margin:0; text-transform:uppercase;">🖥 Total Devices</h3>
        <h1 style="font-size:32px; margin:10px 0 0 0; font-weight:700; font-family:monospace;">44</h1>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # Refactored Interactive Horizontal Architecture Pipeline Diagram
    st.markdown("<p style='font-weight:600; font-size:14px; color:#1e293b; margin-bottom:12px;'>⚡ Big Data Stream Processing Architecture Pipeline</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="
    background:#0f172a;
    padding:20px;
    border-radius:15px;
    color:white;
    font-family: monospace;
    display: flex;
    justify-content: space-around;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    ">
        <span style="background:#334155; padding:8px 12px; border-radius:6px;">📂 Healthcare IoT Dataset</span>
        <span style="color:#60a5fa;">➔</span>
        <span style="background:#1e3a8a; padding:8px 12px; border-radius:6px; border:1px solid #3b82f6;">⚡ PySpark Processing</span>
        <span style="color:#60a5fa;">➔</span>
        <span style="background:#334155; padding:8px 12px; border-radius:6px;">🛠 Feature Engineering</span>
        <span style="color:#60a5fa;">➔</span>
        <span style="background:#1e3a8a; padding:8px 12px; border-radius:6px; border:1px solid #3b82f6;">💾 Parquet Storage</span>
        <span style="color:#60a5fa;">➔</span>
        <span style="background:#334155; padding:8px 12px; border-radius:6px;">📊 Threat Analytics</span>
        <span style="color:#60a5fa;">➔</span>
        <span style="background:#059669; padding:8px 12px; border-radius:6px;">🛡 IoT Guardian Dashboard</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # Dynamic Allocation Plotting View
    attack_dist = pd.DataFrame({
        "Traffic Type": ["Normal", "Attack"],
        "Count": [75997, 56088]
    })

    st.markdown("<p style='font-weight:600; font-size:14px; color:#1e293b; margin-bottom:8px;'>Traffic Distribution Summary Profile</p>", unsafe_allow_html=True)
    attack_fig = px.bar(
        attack_dist,
        x="Traffic Type",
        y="Count",
        color="Traffic Type",
        text="Count",
        color_discrete_map={"Normal": "#14532d", "Attack": "#991b1b"},
        title="Traffic Distribution"
    )
    attack_fig.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(attack_fig, use_container_width=True)


# ==========================================
# TAB 2: DEVICE RISK ANALYTICS
# ==========================================
with tab2:
    st.markdown("<h4 style='color:#1e293b; margin-top:0;'>🖥 Edge Asset Risk Index Configuration</h4>", unsafe_allow_html=True)

    top_devices = (
        device_risk[device_risk["risk_score"] >= 50]
        .sort_values(by="risk_score", ascending=False)
    )

    fig = px.bar(
        top_devices,
        x="ip_src",
        y="risk_score",
        color="risk_score",
        title="Top High-Risk Devices Analysis Pool",
        text="risk_score",
        color_continuous_scale=["#fef08a", "#f97316", "#dc2626"]
    )
    fig.update_layout(
        xaxis_title="Device IP Source Address Vector",
        yaxis_title="Risk Evaluation Score Index",
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("<p style='font-weight:600; font-size:14px; color:#1e293b; margin-bottom:8px;'>🚨 High-Risk Isolated Asset Matrix</p>", unsafe_allow_html=True)
    critical_devices = device_risk[device_risk["risk_level"] == "Critical"]

    st.dataframe(
        critical_devices[["ip_src", "risk_score", "risk_level"]].rename(columns={
            "ip_src": "Source Node IP Address (ip.src)",
            "risk_score": "Aggregated Threat Risk Score",
            "risk_level": "Isolation Severity Classification"
        }),
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# TAB 3: MQTT THREAT INTELLIGENCE
# ==========================================
with tab3:
    st.markdown("<h4 style='color:#1e293b; margin-top:0;'>📡 MQTT Broker & Telemetry Channel Analysis</h4>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("High-Risk Telemetry Topics Identified", "10")
    with col2:
        st.metric("Attack Topics Concentration", "100%")
    with col3:
        st.metric("Peak Channel Attack Velocity", "100%")

    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.error("🚨 **Topic1** \n\n 100% Verified Attack Rate Profile")
    with c2:
        st.warning("⚠️ **$SYS/# Layer** \n\n 100% Attack Injection Rate")
    with c3:
        st.error("🚨 **/../../../../ (Traversal)** \n\n 100% Attack Signature Mapping")

    top_topics = (
        topic_stats[topic_stats["traffic_count"] >= 10]
        .sort_values(by="attack_rate", ascending=False)
        .head(10)
    )

    st.divider()

    #st.markdown("<p style='font-weight:600; font-size:14px; color:#1e293b; margin-bottom:8px;'>MQTT Message Control Block Code Vector Risks</p>", unsafe_allow_html=True)
    msg_fig = px.bar(
        msgtype_stats,
        x="mqtt_msgtype",
        y="attack_rate",
        color="attack_rate",
        text="attack_rate",
        color_continuous_scale=["#cbd5e1", "#3b82f6", "#1e3a8a"],
        title="MQTT Message Operational Type Threat Ratios"
    )
    msg_fig.update_layout(
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(msg_fig, use_container_width=True)

    st.divider()

    st.markdown("""
    <div style="background: #f0fdf4; color: #166534; padding: 18px; border-radius: 12px; border-left: 5px solid #22c55e; font-size: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.02);">
        <h4 style="margin:0 0 8px 0; color:#166534; font-weight:700;">📌 Deep Telemetry Key Findings</h4>
        <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
            <li><b>Topic1</b> registry channel demonstrated absolute (100%) exploit mapping saturation.</li>
            <li>System variables channels such as <code>$SYS/#</code> and root traversal configurations <code>/../../../../</code> function entirely within compromised network clusters.</li>
            <li>MQTT operational message headers <b>0, 5, 8, 9, and 14</b> display structural threat vulnerabilities higher than 90% in relative context environments.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# TAB 4: THREAT INSIGHTS
# ==========================================
with tab4:
    st.markdown("<h4 style='color:#1e293b; margin-top:0;'>🚨 Executive Incident Response Space</h4>", unsafe_allow_html=True)

    # Executive Context Analytics Row Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:#7f1d1d; padding:20px; border-radius:15px; text-align:center; color:white;">
        <h3 style="font-size:14px; color:#fca5a5; margin:0; text-transform:uppercase;">🚨 Critical Devices</h3>
        <h1 style="font-size:32px; margin:10px 0 0 0; font-weight:700; font-family:monospace;">4</h1>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#92400e; padding:20px; border-radius:15px; text-align:center; color:white;">
        <h3 style="font-size:14px; color:#fde047; margin:0; text-transform:uppercase;">⚡ Attack Bursts</h3>
        <h1 style="font-size:32px; margin:10px 0 0 0; font-weight:700; font-family:monospace;">101</h1>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background:#1e3a8a; padding:20px; border-radius:15px; text-align:center; color:white;">
        <h3 style="font-size:14px; color:#93c5fd; margin:0; text-transform:uppercase;">📡 Risky MQTT Types</h3>
        <h1 style="font-size:32px; margin:10px 0 0 0; font-weight:700; font-family:monospace;">5</h1>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # Risk Layout Split Grid Configuration
    left, right = st.columns([2, 1], gap="medium")

    with left:
        risk_dist = device_risk["risk_level"].value_counts().reset_index()
        risk_dist.columns = ["Risk Level", "Count"]

        risk_fig = px.pie(
            risk_dist,
            names="Risk Level",
            values="Count",
            hole=0.6,
            color_discrete_sequence=["#1e3a8a", "#991b1b"],
            title="System Registry Segmentation Distribution Profile"
        )
        risk_fig.update_layout(
            height=380,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(risk_fig, use_container_width=True)

    with right:
        st.write("")
        st.success("✅ 40 Normal/Low-Risk Connected Nodes")
        st.error("🚨 4 Critical Isolated Threat Targets")

        st.markdown("""
        <div style="background: white; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0; margin-top: 10px; font-size: 13px; color:#475569; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            ℹ️ <b>Operational Volume Matrix:</b> Critical categorized edge points isolate exactly <b>~9%</b> of active healthcare physical assets within monitoring frames.
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Core Comprehensive Findings Section
    st.markdown("""
    <div style="background: #eff6ff; color: #1e3a8a; padding: 22px; border-radius: 15px; border-left: 6px solid #1e3a8a; box-shadow: 0 4px 12px rgba(0,0,0,0.04);">
        <h3 style="margin:0 0 12px 0; color:#1e293b; font-size:18px; font-weight:700;">📋 Tactical Performance Execution Findings</h3>
        <ul style="margin: 0; padding-left: 20px; line-height: 1.7; font-size: 14px; color:#1e293b;">
            <li>Four physical infrastructure components are routed to <b>Critical Quarantine Isolation zones</b>.</li>
            <li>MQTT directory streams including <code>Topic1</code>, <code>$SYS/#</code>, and directory-traversal matrices display confirmed threat injection profiles.</li>
            <li>MQTT transmission structural blocks <b>0, 5, 8, 9, and 14</b> mapped anomalous packet behaviors above 90% bounds.</li>
            <li>Temporal analytics window indexes validated fast threat injection spikes exceeding <b>100 packets per sequence</b>.</li>
            <li><b>PySpark distributed framework architecture</b> executed successfully, compiling core intelligence arrays from streaming telemetry files cleanly.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# --- Footer Module Match ---
st.markdown("""
<div style="text-align:center; padding:40px 0 20px 0; color:gray; font-size:12px;">
BSD Elective Project • IoT Guardian • UMPSA Data Analytics
</div>
""", unsafe_allow_html=True)