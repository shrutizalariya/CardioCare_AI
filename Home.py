import streamlit as st
import pandas as pd
import pickle
import numpy as np
from fpdf import FPDF
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="CardioCare AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- FLAT MODERN DESIGN SYSTEM ---
def apply_flat_design():
    """Apply clean, flat modern design with no glassmorphism"""
    dark = st.session_state.get("dark_mode", False)
    
    # Flat color palette
    if dark:
        bg_color = "#1a1a1a"  # Deep charcoal
        card_bg = "#2d2d2d"
        text_color = "#e5e5e5"
        border_color = "#404040"
        primary_red = "#dc2626"
    else:
        bg_color = "#f5f5f5"  # Light gray
        card_bg = "#ffffff"  # White
        text_color = "#1a1a1a"
        border_color = "#d4d4d4"
        primary_red = "#dc2626"
    
    st.markdown(f"""
    <style>
    /* Hide sidebar completely */
    [data-testid='stSidebar'] {{
        display: none !important;
    }}
    
    /* Main app background - flat */
    .stApp {{
        background: {bg_color};
        color: {text_color};
    }}
    
    /* Block container */
    .main .block-container {{
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }}
    
    /* Top navigation bar */
    .top-nav {{
        background: {card_bg};
        border-bottom: 2px solid {border_color};
        padding: 1rem 2rem;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 0;
    }}
    
    .nav-links {{
        display: flex;
        gap: 1rem;
    }}
    
    .nav-link {{
        padding: 0.5rem 1.5rem;
        background: {card_bg};
        border: 2px solid {border_color};
        border-radius: 12px;
        color: {text_color};
        text-decoration: none;
        font-weight: 600;
        transition: all 0.2s;
        cursor: pointer;
    }}
    
    .nav-link:hover {{
        background: {primary_red};
        color: white;
        border-color: {primary_red};
    }}
    
    .nav-link.active {{
        background: {primary_red};
        color: white;
        border-color: {primary_red};
    }}
    
    /* Flat cards - no blur, sharp borders */
    .flat-card {{
        background: {card_bg};
        border: 2px solid {border_color};
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }}
    
    /* Headings */
    h1, h2, h3, h4 {{
        color: {primary_red} !important;
        font-weight: 700;
    }}
    
    /* Buttons - flat design */
    .stButton > button {{
        background: {primary_red};
        color: white;
        border: 2px solid {primary_red};
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem 2rem;
        transition: all 0.2s;
    }}
    
    .stButton > button:hover {{
        background: #b91c1c;
        border-color: #b91c1c;
        box-shadow: 0 2px 4px rgba(220, 38, 38, 0.3);
    }}
    
    /* Input fields */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {{
        background-color: {card_bg};
        color: {text_color};
        border: 2px solid {border_color};
        border-radius: 8px;
    }}
    
    /* Heart scoreboard - flat */
    .heart-scoreboard {{
        display: flex;
        justify-content: center;
        gap: 1rem;
        font-size: 2rem;
        padding: 1.5rem;
        background: {card_bg};
        border: 2px solid {border_color};
        border-radius: 12px;
        margin: 1.5rem 0;
    }}
    
    /* Checkbox styling */
    .stCheckbox > label {{
        font-weight: 500;
    }}
    
    /* Theme toggle button */
    .theme-toggle {{
        padding: 0.5rem 1rem;
        background: {card_bg};
        border: 2px solid {border_color};
        border-radius: 8px;
        color: {text_color};
        cursor: pointer;
    }}
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

apply_flat_design()

# --- TOP NAVIGATION ---
def render_top_nav():
    """Render top navigation bar"""
    dark = st.session_state.get("dark_mode", False)
    current_page = st.session_state.get("current_page", "Dashboard")
    
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    
    with col1:
        st.markdown("### 🫀 CardioCare AI")
    
    with col2:
        if st.button("📊 Dashboard", use_container_width=True, 
                    type="primary" if current_page == "Dashboard" else "secondary"):
            st.session_state.current_page = "Dashboard"
            st.rerun()
    
    with col3:
        if st.button("📈 Analytics", use_container_width=True,
                    type="primary" if current_page == "Analytics" else "secondary"):
            st.session_state.current_page = "Analytics"
            st.switch_page("pages/2_Clinical_Analytics.py")
    
    with col4:
        if st.button("👤 Researcher", use_container_width=True,
                    type="primary" if current_page == "Researcher" else "secondary"):
            st.session_state.current_page = "Researcher"
            st.switch_page("pages/3_Researcher_Info.py")
    
    with col5:
        if st.button("🌙" if not dark else "☀️", use_container_width=True):
            st.session_state.dark_mode = not dark
            st.rerun()

# Render navigation
render_top_nav()

# --- PDF GENERATION ---
def generate_pdf(user_data, prediction, score, suggestions, risk_enhancers):
    """Generate professional PDF report"""
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(220, 38, 38)
    pdf.cell(200, 10, "CardioCare AI - Clinical Report", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)
    
    # Prediction Result
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(220, 38, 38)
    result_text = "HIGH CARDIOVASCULAR RISK" if prediction == 1 else "LOW CARDIOVASCULAR RISK"
    pdf.cell(200, 10, result_text, ln=True, align='C')
    pdf.ln(8)
    
    # Heart Score
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 8, f"Heart Health Score: {score}/7", ln=True)
    pdf.ln(5)
    
    # Patient Information
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 8, "Patient Information:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 6, f"Age: {user_data['Age']} years", ln=True)
    pdf.cell(200, 6, f"Gender: {user_data['Gender']}", ln=True)
    pdf.cell(200, 6, f"Height: {user_data['Height']} cm | Weight: {user_data['Weight']} kg", ln=True)
    pdf.cell(200, 6, f"BMI: {user_data['BMI']:.1f}", ln=True)
    pdf.cell(200, 6, f"Blood Pressure: {user_data['Systolic BP']}/{user_data['Diastolic BP']} mmHg", ln=True)
    pdf.cell(200, 6, f"Cholesterol: {user_data['Cholesterol']} | Glucose: {user_data['Glucose']}", ln=True)
    pdf.ln(5)
    
    # Risk Enhancers
    if risk_enhancers:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 8, "Clinical Risk Enhancers:", ln=True)
        pdf.set_font("Arial", size=10)
        for enhancer in risk_enhancers:
            pdf.cell(200, 6, f"• {enhancer}", ln=True)
        pdf.ln(5)
    
    # Recommendations
    if suggestions:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 8, "Recommendations:", ln=True)
        pdf.set_font("Arial", size=10)
        for suggestion in suggestions[:8]:  # Limit for PDF
            pdf.cell(200, 6, f"• {suggestion}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 5, "Disclaimer: Educational purposes only. Not a substitute for medical advice.", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- HEALTHY HEART SCOREBOARD ---
def calculate_heart_score(age, gender, height, weight, ap_hi, ap_lo, chol, gluc, smoke, alco, active):
    """Calculate heart health score (0-7)"""
    score = 0
    bmi = weight / ((height/100)**2)
    
    if not smoke: score += 1
    if not alco: score += 1
    if active: score += 1
    if 18.5 <= bmi <= 24.9: score += 1
    if chol == 1: score += 1
    if gluc == 1: score += 1
    if ap_hi < 130 and ap_lo < 80: score += 1
    
    return score, bmi

# --- DYNAMIC HEALTH INSIGHTS ---
def get_health_insights(prediction, age, bmi, ap_hi, ap_lo, chol, gluc, smoke, alco, active, risk_enhancers):
    """Generate personalized health insights"""
    insights = []
    
    if prediction == 1:
        insights.append("⚠️ HIGH RISK: Consult a healthcare professional immediately.")
        
        if smoke:
            insights.append("🚭 QUIT SMOKING: Reduces heart disease risk by 50% within one year.")
        
        if ap_hi >= 140 or ap_lo >= 90:
            insights.append("🩺 MANAGE BP: Reduce sodium, increase potassium-rich foods.")
        
        if bmi > 25:
            insights.append(f"⚖️ WEIGHT MANAGEMENT: BMI {bmi:.1f}. Aim for 18.5-24.9.")
        
        if chol > 1:
            insights.append("💊 LOWER CHOLESTEROL: Reduce saturated fats, increase fiber.")
        
        if gluc > 1:
            insights.append("🍯 CONTROL GLUCOSE: Limit refined sugars and carbs.")
        
        if not active:
            insights.append("🏃 EXERCISE: Aim for 150 minutes/week of moderate activity.")
        
        if alco:
            insights.append("🍷 REDUCE ALCOHOL: Limit or eliminate consumption.")
        
        if risk_enhancers:
            insights.append(f"⚠️ ADDITIONAL RISK FACTORS: {len(risk_enhancers)} clinical enhancer(s) identified.")
    else:
        insights.append("✅ LOW RISK: Maintain your healthy lifestyle.")
        if bmi > 24.9:
            insights.append("💪 Consider maintaining optimal weight.")
        if not active:
            insights.append("🏃 Add regular physical activity for optimal health.")
    
    return insights

# --- MAIN DASHBOARD CONTENT ---
st.markdown("## 📊 Cardiovascular Risk Assessment Dashboard")

# Clinical Input Form
st.markdown("### Clinical Data Input")

col1, col2, col3 = st.columns(3)

with col1:
    age_years = st.number_input("Age (Years)", min_value=1, max_value=110, value=35, step=1)
    gender_str = st.selectbox("Gender", ["Female", "Male"])
    height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170, step=1)
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=250.0, value=70.0, step=0.1)

with col2:
    ap_hi = st.number_input("Systolic BP (mmHg)", min_value=80, max_value=220, value=120, step=1)
    ap_lo = st.number_input("Diastolic BP (mmHg)", min_value=40, max_value=120, value=80, step=1)
    cholesterol = st.selectbox(
        "Cholesterol Level",
        [1, 2, 3],
        format_func=lambda x: {1: "Normal", 2: "Above Normal", 3: "High"}[x]
    )
    glucose = st.selectbox(
        "Glucose Level",
        [1, 2, 3],
        format_func=lambda x: {1: "Normal", 2: "Above Normal", 3: "High"}[x]
    )

with col3:
    smoke = st.checkbox("🚬 Smoking Habit")
    alco = st.checkbox("🍷 Alcohol Intake")
    active = st.checkbox("💪 Physically Active")
    st.markdown("---")
    st.caption("💡 Enter accurate clinical data for best results")

# Clinical Risk Enhancers Section
st.markdown("### Clinical Risk Enhancers")
enhancer_col1, enhancer_col2 = st.columns(2)

with enhancer_col1:
    family_history = st.checkbox("Family History of Heart Disease")
    kidney_disease = st.checkbox("Chronic Kidney Disease")

with enhancer_col2:
    metabolic_syndrome = st.checkbox("Metabolic Syndrome")
    inflammatory_conditions = st.checkbox("Chronic Inflammatory Conditions")

# Collect risk enhancers
risk_enhancers = []
if family_history:
    risk_enhancers.append("Family History of Heart Disease")
if kidney_disease:
    risk_enhancers.append("Chronic Kidney Disease")
if metabolic_syndrome:
    risk_enhancers.append("Metabolic Syndrome")
if inflammatory_conditions:
    risk_enhancers.append("Chronic Inflammatory Conditions")

# Prediction Button
if st.button("🚀 Analyze Cardiovascular Risk", use_container_width=True, type="primary"):
    try:
        # Load model
        with open("heart_model.pkl", "rb") as f:
            model = pickle.load(f)
        
        # Convert inputs - match training data order: [age, gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active]
        age_days = age_years * 365
        gender_num = 1 if gender_str == "Female" else 2
        
        input_data = np.array([[
            age_days, gender_num, height, weight, ap_hi, ap_lo,
            cholesterol, glucose, int(smoke), int(alco), int(active)
        ]])
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        
        # Calculate metrics
        heart_score, bmi = calculate_heart_score(
            age_years, gender_num, height, weight, ap_hi, ap_lo,
            cholesterol, glucose, smoke, alco, active
        )
        
        # Get health insights
        insights = get_health_insights(
            prediction, age_years, bmi, ap_hi, ap_lo,
            cholesterol, glucose, smoke, alco, active, risk_enhancers
        )
        
        # Store in session state
        st.session_state.prediction_result = {
            'prediction': prediction,
            'score': heart_score,
            'bmi': bmi,
            'insights': insights,
            'risk_enhancers': risk_enhancers
        }
        
        st.rerun()
        
    except FileNotFoundError:
        st.error("⚠️ Error: 'heart_model.pkl' not found.")
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

# Display Results
if 'prediction_result' in st.session_state:
    result = st.session_state.prediction_result
    
    st.markdown("---")
    
    # Prediction Result
    if result['prediction'] == 1:
        st.error("### ⚠️ High Cardiovascular Risk Detected")
    else:
        st.success("### ✅ Low Cardiovascular Risk Detected")
    
    # Healthy Heart Scoreboard
    st.markdown("### 🌟 Healthy Heart Scoreboard")
    heart_icons = " ".join(["❤️" if i < result['score'] else "🤍" for i in range(7)])
    st.markdown(f"""
    <div class="heart-scoreboard">
        {heart_icons}
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**Score: {result['score']}/7**")
    
    # Dynamic Health Insights
    st.markdown("### 💡 Dynamic Health Insights")
    for insight in result['insights']:
        if "HIGH RISK" in insight or "⚠️" in insight:
            st.warning(insight)
        elif "✅" in insight:
            st.success(insight)
        else:
            st.info(insight)
    
    # Risk Enhancers Display
    if result['risk_enhancers']:
        st.markdown("### ⚠️ Clinical Risk Enhancers Identified")
        for enhancer in result['risk_enhancers']:
            st.warning(f"• {enhancer}")
    
    # PDF Export
    user_data = {
        'Age': age_years,
        'Gender': gender_str,
        'Height': height,
        'Weight': weight,
        'BMI': result['bmi'],
        'Systolic BP': ap_hi,
        'Diastolic BP': ap_lo,
        'Cholesterol': {1: "Normal", 2: "Above Normal", 3: "High"}[cholesterol],
        'Glucose': {1: "Normal", 2: "Above Normal", 3: "High"}[glucose],
        'Smoking': smoke,
        'Alcohol': alco,
        'Active': active
    }
    
    pdf_bytes = generate_pdf(user_data, result['prediction'], result['score'], result['insights'], result['risk_enhancers'])
    st.download_button(
        "📥 Generate Clinical Report (PDF)",
        pdf_bytes,
        file_name=f"CardioCare_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

# Footer
st.markdown("---")
st.caption("💡 **Note:** This tool is for educational purposes only. Always consult healthcare professionals for medical advice.")
