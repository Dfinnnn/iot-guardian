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

st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        180deg,
        #f8fafc 0%,
        #e2e8f0 100%
    );
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div style="
background:linear-gradient(90deg,#0f172a,#1e3a8a);
padding:35px;
border-radius:20px;
text-align:center;
color:white;
">
<h1>🛡️ IoT Guardian</h1>
<h3>AI-Powered Threat Detection for Smart Healthcare</h3>
<p>
Deep Learning • Big Data Analytics • Explainable AI
</p>
</div>
""", unsafe_allow_html=True)

st.divider()
st.markdown("""
<div style="
background:white;
padding:20px;
border-radius:15px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
margin-bottom:20px;
text-align:center;
">
<h3>System Overview</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="
    background:#1e293b;
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;">
    <h3>📦 Records</h3>
    <h1>132,085</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
    background:#991b1b;
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;">
    <h3>🚨 Attacks</h3>
    <h1>56,088</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="
    background:#1e293b;
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;">
    <h3>🖥 Devices</h3>
    <h1>44</h1>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="
    background:#1e3a8a;
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;">
    <h3>🧠 AI Model</h3>
    <h1>MLP</h1>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.markdown("""
<div style="
background:white;
padding:20px;
border-radius:15px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
margin-bottom:20px;
text-align:center;
">
<h3>System Architecture</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background:#0f172a;
padding:30px;
border-radius:20px;
color:white;
text-align:center;
font-size:20px;
">

📂 Healthcare IoT Dataset

        ⬇️

⚡ PySpark Analytics

        ⬇️

🧠 Deep Learning (MLP)

        ⬇️

🔍 SHAP Explainability

        ⬇️

🛡️ IoT Guardian Dashboard

</div>
""", unsafe_allow_html=True)

st.divider()

st.markdown("""
<div style="
background:white;
padding:20px;
border-radius:15px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
margin-bottom:20px;
text-align:center;
">
<h3>Project Modules</h3>
</div>
""", unsafe_allow_html=True)


c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown("""
    <div style="
    background:#1e293b;
    padding:20px;
    border-radius:18px;
    color:white;
    height:220px;
    ">

    <h2 style="
    font-size:22px;
    margin-bottom:10px;
    line-height:1.3;
    ">
    🧠 Live Threat Monitor
    </h2>

    <p style="
    color:#facc15;
    font-size:14px;
    font-weight:600;
    ">
    Real-Time Threat Detection
    </p>

    <p style="
    color:#cbd5e1;
    font-size:13px;
    line-height:1.6;
    ">
    Monitors healthcare IoT traffic and identifies malicious activity using deep learning models.
    </p>

    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown("""
    <div style="
    background:#1e293b;
    padding:20px;
    border-radius:18px;
    color:white;
    height:220px;
    ">
                
    <h2 style="
    font-size:22px;
    margin-bottom:10px;
    line-height:1.3;
    ">
    🖥️ Device Risk Centre
    </h2>

    <p style="
    color:#facc15;
    font-size:14px;
    font-weight:600;
    ">
    Device Risk Assessment
    </p>

    <p style="
    color:#cbd5e1;
    font-size:13px;
    line-height:1.6;
    ">
    Evaluates device behaviour and prioritises high-risk assets within the healthcare network.
    </p>

    </div>
    """, unsafe_allow_html=True)

with c3:

    st.markdown("""
    <div style="
    background:#1e293b;
    padding:20px;
    border-radius:18px;
    color:white;
    height:220px;
    ">
                
    <h2 style="
    font-size:22px;
    margin-bottom:10px;
    line-height:1.3;
    ">
    ⚡ Big Data Pipeline
    </h2>
                
    <p style="
    color:#facc15;
    font-size:14px;
    font-weight:600;
    ">
    Scalable Threat Analytics
    </p>

    <p style="
    color:#cbd5e1;
    font-size:13px;
    line-height:1.6;
    ">
    Processes large-scale MQTT traffic using PySpark for security analytics and intelligence generation.
    </p>

    </div>
    """, unsafe_allow_html=True)

with c4:

    st.markdown("""
    <div style="
    background:#1e293b;
    padding:20px;
    border-radius:18px;
    color:white;
    height:220px;
    ">
                
    <h2 style="
    font-size:22px;
    margin-bottom:10px;
    line-height:1.3;
    ">
    🔍 AI Explainability Centre
    </h2>

    <p style="
    color:#facc15;
    font-size:14px;
    font-weight:600;
    ">
    Transparent AI Decisions
    </p>

    <p style="
    color:#cbd5e1;
    font-size:13px;
    line-height:1.6;
    ">
    Provides interpretable explanations for model predictions using SHAP and feature importance analysis.
    </p>

    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown("""
<div style="
background:white;
padding:20px;
border-radius:15px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
margin-bottom:20px;
text-align:center;
">
<h3>Technologies Used</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background:#e0e7ff;
padding:20px;
border-radius:15px;
font-size:18px;
line-height:2;
">

🧠 <b>Machine Learning</b>: Random Forest • MLP • GRU<br>

⚡ <b>Big Data</b>: PySpark • Parquet<br>

📊 <b>Dashboard</b>: Streamlit • Plotly<br>

🔍 <b>Explainability</b>: SHAP<br>

💻 <b>Programming</b>: Python

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
text-align:center;
padding:20px;
color:gray;">
BSD Elective Project • IoT Guardian • UMPSA Data Analytics
</div>
""", unsafe_allow_html=True)