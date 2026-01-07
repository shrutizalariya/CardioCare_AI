import streamlit as st
import pandas as pd
import pickle
import numpy as np
import base64

# --- PAGE CONFIG ---
st.set_page_config(page_title="CardioCare AI", page_icon="❤️", layout="wide", initial_sidebar_state="collapsed")

# --- CSS TO HIDE SIDEBAR & STYLE TOP NAV ---
def apply_styling():
    dark = st.session_state.get("dark_mode", True)
    bg = "radial-gradient(circle at top, #020617, #000)" if dark else "linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%)"
    card_bg = "rgba(30, 41, 59, 0.7)" if dark else "rgba(255, 255, 255, 0.8)"
    text = "#f8fafc" if dark else "#0f172a"
    
    st.markdown(f"""
    <style>
    /* Hide Sidebar */
    [data-testid="stSidebar"] {{ display: none; }}
    [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
    
    .stApp {{ background: {bg}; color: {text}; font-family: 'Inter', sans-serif; }}
    
    /* Top Navigation Bar */
    .nav-bar {{
        display: flex; justify-content: space-between; align-items: center;
        padding: 15px 30px; background: {card_bg}; backdrop-filter: blur(10px);
        border-radius: 15px; margin-bottom: 30px; border: 1px solid rgba(255,255,255,0.1);
    }}
    
    .glass-card {{
        background: {card_bg}; backdrop-filter: blur(12px);
        border-radius: 24px; padding: 35px; border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2); margin-bottom: 25px;
    }}
    
    h1, h2, h3 {{ color: #ef4444 !important; font-weight: 800; }}
    
    .stButton button {{
        background: linear-gradient(135deg, #ef4444, #b91c1c);
        color: white; border-radius: 14px; border: none; padding: 12px;
        font-weight: bold; width: 100%; transition: 0.3s ease;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if "dark_mode" not in st.session_state: st.session_state.dark_mode = True

apply_styling()

# --- TOP NAVIGATION & HEADER ---
st.markdown("""<div class="nav-bar">
    <div style="display: flex; align-items: center; gap: 15px;">
        <img src="https://cdn-icons-png.flaticon.com/512/833/833472.png" width="40">
        <span style="font-size: 24px; font-weight: bold; color: #ef4444;">CardioCare AI</span>
    </div>
</div>""", unsafe_allow_html=True)

# Theme Toggle placed in a layout column for accessibility
t1, t2 = st.columns([9, 1])
with t2:
    st.session_state.dark_mode = st.toggle("🌙", value=st.session_state.dark_mode)

# --- MAIN CONTENT ---
st.markdown("<div class='glass-card'><h1>🫀 Diagnostic Dashboard</h1><p>Predictive engine for cardiovascular health based on 70,000 clinical records.</p></div>", unsafe_allow_html=True)

# Input Form in Cards
with st.container():
    st.subheader("📋 Patient Metrics")
    c1, c2, c3 = st.columns(3)
    with c1:
        age_yr = st.number_input("Age (Years)", 18, 100, 45)
        gender = st.selectbox("Gender", ["Female", "Male"])
        height = st.number_input("Height (cm)", 120, 220, 165)
    with c2:
        weight = st.number_input("Weight (kg)", 40.0, 180.0, 70.0)
        hi = st.number_input("Systolic (ap_hi)", 80, 200, 120)
        lo = st.number_input("Diastolic (ap_lo)", 50, 120, 80)
    with c3:
        chol = st.selectbox("Cholesterol", [1, 2, 3], format_func=lambda x: ["Normal", "Borderline", "High"][x-1])
        gluc = st.selectbox("Glucose", [1, 2, 3], format_func=lambda x: ["Normal", "Borderline", "High"][x-1])

st.markdown("---")
l1, l2, l3 = st.columns([1,1,2])
smoke = l1.checkbox("Smoking History")
active = l2.checkbox("Regular Activity")

if st.button("🔍 START SCAN"):
    try:
        # Load and Predict
        with open("heart_model.pkl", "rb") as f: model = pickle.load(f)
        gen_val = 1 if gender == "Female" else 2
        bmi = weight / ((height/100)**2)
        features = np.array([[age_yr*365, gen_val, height, weight, hi, lo, chol, gluc, int(smoke), 0, int(active)]])
        prediction = model.predict(features)

        # Result Card
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if prediction[0] == 1:
            st.error("### ⚠️ Result: High Risk Profile")
        else:
            st.success("### ✅ Result: Low Risk Profile")
            
        # Scoreboard
        st.subheader("🌟 Heart Health Scoreboard")
        score = sum([not smoke, active, 18.5<=bmi<=25, chol==1, gluc==1, hi<130, lo<85])
        sc_cols = st.columns(7)
        for i in range(7): sc_cols[i].markdown("❤️" if i < score else "🤍")
        st.info(f"Met **{score} out of 7** healthy cardiovascular markers.")
        
    except:

        st.warning("Please ensure 'heart_model.pkl' is in the project folder.")
