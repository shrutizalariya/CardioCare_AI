import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import datetime, os

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="CardioSense", page_icon="🫀", layout="wide")

# --------------------------------------------------
# THEME STATE
# --------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

def theme_icon():
    return "🌙" if st.session_state.theme == "Light" else "☀️"

def apply_theme():
    if st.session_state.theme == "Dark":
        bg = "#020617"
        card = "#1C1C2E"
        text = "#FFFFFF"
        border = "#44475A"
    else:
        bg = "#FAFAFC"
        card = "#FFFFFF"
        text = "#1F2937"
        border = "#E5E7EB"

    st.markdown(f"""
    <style>
    .stApp {{
        background: {bg};
        color: {text};
        font-family: "Segoe UI", sans-serif;
    }}
    .logo {{
        font-size:30px;
        font-weight:800;
        color:{text};
    }}
    .glass {{
        background:{card};
        padding:26px;
        border-radius:18px;
        border:1px solid {border};
        box-shadow:0 12px 30px rgba(0,0,0,0.12);
        margin-bottom:28px;
    }}
    h1, h2, h3, h4, p, ul, ol {{
        color:{text};
    }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# --------------------------------------------------
# SAMPLE MODEL DATA (df_models)
# --------------------------------------------------
df_models = pd.DataFrame({
    "Model": ["XGBoost", "Random Forest", "KNN", "Logistic Regression"],
    "Training Accuracy": [78.5, 76.2, 72.5, 70.1],
    "Testing Accuracy": [74.3, 71.8, 69.5, 68.2],
    "Precision (%)": [76.0, 73.5, 70.2, 69.0],
    "Recall (%)": [75.5, 72.0, 68.9, 67.5]
})

# --------------------------------------------------
# TOP NAVIGATION BAR
# --------------------------------------------------
nav1, nav2 = st.columns([8, 2])
with nav1:
    st.markdown("<div class='logo'>🫀 CardioSense</div>", unsafe_allow_html=True)
with nav2:
    if st.button(f"{theme_icon()}"):
        st.session_state.theme = "Dark" if st.session_state.theme == "Light" else "Light"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# TOP TABS
# --------------------------------------------------
tabs = st.tabs([
    "🏠 Home",
    "⚠️ Disclaimer",
    "📘 About",
    "🔐 Ethics",
    "❓ Help",
    "📊 Model Performance",
    "Risk Predictor",
    "Researcher info"
])

# --------------------------------------------------
# HOME
# --------------------------------------------------
with tabs[0]:
    st.markdown("""
    ### 🫀 AI-Driven Heart Risk Assessment

    CardioSense is an artificial intelligence based system designed to provide
    early awareness of cardiovascular disease risk.

    The system analyzes selected health parameters and generates
    a risk indication using machine learning techniques.
    """)
    st.markdown("""
<div class="glass">
<b>⚠️ Important Note</b><br>
This application is intended strictly for educational and research purposes.
It does not replace professional medical diagnosis or treatment.
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# DISCLAIMER
# --------------------------------------------------
with tabs[1]:
    st.markdown("""
<div class="glass">
<h2 style="text-align:center; color:#dc2626;">⚠️ Critical Medical Disclaimer</h2>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="glass">
<h3>📋 Important Notice</h3>
<p>
CardioSense predictions are based on <strong>historical health data patterns</strong>. 
Machine learning models <strong>cannot replace</strong> physical examinations or professional medical judgment.
</p>
<p>
Model accuracy is approximately <strong>73.2%</strong>. 
<strong>False positives and false negatives are possible.</strong>
</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="emergency-box">
    <h2 style="color: #dc2626; margin-bottom: 15px;">🚑 Emergency Situations</h2>
    <p style="font-size: 18px; font-weight: 600;">
        If you are experiencing <strong>chest pain, shortness of breath, dizziness, 
        or any acute cardiac symptoms</strong>, do NOT use this application.
    </p>
    <p style="font-size: 20px; font-weight: 700; margin-top: 15px;">
        Call your local emergency services (911, 112, or your local emergency number) immediately.
    </p>
</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.subheader("🏥 For Educational Use Only")
        st.markdown("""
        - Tool is for **educational and awareness purposes** only
        - Results should be interpreted with caution
        - Do not use predictions to self-diagnose or self-treat
        - Consult healthcare professionals for medical decisions
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.subheader("📊 Model Limitations")
        st.markdown("""
        - Accuracy ~73.2% (not 100% reliable)
        - Based on historical data only
        - Cannot detect all cardiovascular conditions
        - May not apply to all demographics equally
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("🔐 Data Privacy & Ethics")
    with st.expander("View Privacy Information", expanded=False):
        st.info("""
        - All input data is processed locally; we do NOT store or transmit your health data.
        - Avoid entering sensitive info on public networks.
        - Use for academic and educational purposes only.
        - Developers assume no liability for medical decisions based on predictions.
        """)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("✅ User Acknowledgment & Consent")
    st.markdown("""
    By using CardioSense, you acknowledge:
    - Tool is educational only
    - Not a substitute for medical advice
    - Consult healthcare professionals
    - Developers are not liable for medical outcomes
    """)

    acknowledged = st.checkbox(
        "**I have read and understood this disclaimer. I acknowledge that this tool is NOT for clinical diagnosis.**",
        key="disclaimer_ack"
    )

    if acknowledged:
        st.success("✅ Thank you. You may proceed responsibly.")
    else:
        st.warning("⚠️ Please acknowledge the medical disclaimer to use the app.")

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# ABOUT
# --------------------------------------------------
with tabs[2]:
    st.markdown("""
<div class="glass">
## 📘 About the Project
This project was developed as part of an academic curriculum
to demonstrate the application of machine learning in healthcare.
<b>Project Objectives:</b>
<ul>
<li>Predict cardiovascular disease risk</li>
<li>Apply machine learning to medical data</li>
<li>Create a professional medical UI</li>
<li>Promote early health awareness</li>
</ul>
</div>
""", unsafe_allow_html=True)
   

    # ---------------- DATASET OVERVIEW ----------------
    st.markdown("<div class='glass'><h3>📊 Dataset Overview</h3></div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Records", "70,000")
    c2.metric("Total Features", "11")
    c3.metric("Target Classes", "Binary (0 / 1)")
    c4.metric("Dataset Health", "98%", "Cleaned")

    st.markdown("<div class='glass'><h4>🧾 Feature Description</h4></div>", unsafe_allow_html=True)

    feature_df = pd.DataFrame({
        "Feature": ["Age", "Gender", "Height", "Weight", "Ap_Hi", "Ap_Lo",
                    "Cholesterol", "Glucose", "Smoke", "Alcohol", "Physical Activity"],
        "Description": [
            "Age of patient (in days)",
            "Biological sex (1: Female, 2: Male)",
            "Height in centimeters",
            "Weight in kilograms",
            "Systolic blood pressure",
            "Diastolic blood pressure",
            "Cholesterol level (Normal → High)",
            "Glucose level (Normal → High)",
            "Smoking habit",
            "Alcohol intake",
            "Regular physical activity"
        ]
    })

    st.dataframe(feature_df, use_container_width=True, hide_index=True)

    with st.expander("👀 View Sample Raw Dataset"):
        st.info("Sample rows from cardio_train.csv used for training")
        sample_df = pd.DataFrame({
            "age": [18393, 20228, 18857],
            "gender": [2, 1, 1],
            "height": [168, 156, 165],
            "weight": [62.0, 85.0, 64.0],
            "ap_hi": [110, 140, 130],
            "ap_lo": [80, 90, 70],
            "cardio": [0, 1, 1]
        })
        st.dataframe(sample_df, use_container_width=True)

    # ---------------- WORKFLOW ----------------
    st.markdown("<div class='glass'><h3>⚙️ Technical Workflow</h3></div>", unsafe_allow_html=True)

    st.success("✅ **Data Cleaning** – Removed invalid blood pressure outliers")
    st.success("✅ **Exploratory Analysis** – Studied age, weight, and BP correlations")
    st.success("✅ **Feature Scaling** – Normalized numeric features")
    st.success("✅ **Model Training** – Evaluated multiple ML algorithms")

    # ---------------- MODEL ARCHITECTURE ----------------
    st.markdown("<div class='glass'><h3>🧠 Model Architecture</h3></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        <div class="glass">
        <h4>Algorithms Evaluated</h4>
        <ul>
            <li>K-Nearest Neighbors (KNN)</li>
            <li>Random Forest Classifier</li>
            <li>Gradient Boosting</li>
            <li><b>XGBoost (Selected)</b></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="glass">
        <h4>XGBoost Configuration</h4>
        <ul>
            <li>Learning Rate: 0.1</li>
            <li>Max Depth: 5</li>
            <li>Estimators: 100</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# ETHICS
# --------------------------------------------------
with tabs[3]:
    st.markdown("""
<div class="glass">
## 🔐 Ethics & Privacy
<ul>
<li>No personal data is stored</li>
<li>No third-party data sharing</li>
<li>Local processing only</li>
<li>Transparency in limitations</li>
</ul>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HELP
# --------------------------------------------------
with tabs[4]:
    st.markdown("""
<div class="glass">
<h2>❓ Help & Instructions</h2>
<ol>
<li>Enter patient parameters</li>
<li>Generate medical report</li>
<li>Download PDF</li>
<li>Consult doctor if required</li>
</ol>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# MODEL PERFORMANCE
# --------------------------------------------------
with tabs[5]:
    import plotly.express as px
    import plotly.graph_objects as go
    from sklearn.metrics import confusion_matrix
    import pandas as pd
    import numpy as np

    # =========================================================
    # HEADER
    # =========================================================
    st.markdown("## 📊 Model Performance & Benchmarking")

    # =========================================================
    # BEST MODEL METRICS (FROM df_models)
    # =========================================================
    winner = df_models[df_models["Model"] == "XGBoost"].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Best Model", "XGBoost")
    c2.metric("Testing Accuracy", f"{winner['Testing Accuracy']:.2f}%")
    c3.metric("Precision", f"{winner['Precision (%)']:.2f}%")
    c4.metric("Recall", f"{winner['Recall (%)']:.2f}%")

    # =========================================================
    # TESTING ACCURACY BAR (SLIM & COLORFUL)
    # =========================================================
    st.markdown("### 📊 Testing Accuracy Comparison")

    fig_bar = px.bar(
        df_models,
        x="Model",
        y="Testing Accuracy",
        text=df_models["Testing Accuracy"].round(1),
        height=260,
        color="Model",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(
        yaxis_title="Accuracy (%)",
        xaxis_title="",
        showlegend=False,
        margin=dict(t=20, b=10)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # =========================================================
    # TRAIN VS TEST ACCURACY
    # =========================================================
    st.markdown("### 📉 Training vs Testing Accuracy")

    fig_compare = go.Figure()
    fig_compare.add_bar(
        x=df_models["Model"],
        y=df_models["Training Accuracy"],
        name="Training",
        marker_color="#3b82f6"
    )
    fig_compare.add_bar(
        x=df_models["Model"],
        y=df_models["Testing Accuracy"],
        name="Testing",
        marker_color="#22c55e"
    )

    fig_compare.update_layout(
        barmode="group",
        height=260,
        yaxis_title="Accuracy (%)",
        margin=dict(t=20, b=10)
    )
    st.plotly_chart(fig_compare, use_container_width=True)

    # Static values (from Jupyter final_model output)
    cm = np.array([
        [4850, 1650],
        [1520, 4980]
    ])

    st.markdown("### 🔍 Confusion Matrix – Final Model (XGBoost)")

    fig_cm = go.Figure(
        data=go.Heatmap(
            z=cm,
            x=["Predicted Low", "Predicted High"],
            y=["Actual Low", "Actual High"],
            colorscale=[
                [0, "#fef2f2"],
                [0.5, "#fecaca"],
                [1, "#dc2626"]
            ],
            text=cm,
            texttemplate="%{text}",
            textfont={"size": 16, "color": "white"}
        )
    )

    fig_cm.update_layout(
        title="XGBoost Confusion Matrix",
        title_x=0.5,
        xaxis_title="Predicted",
        yaxis_title="Actual",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=360
    )

    st.plotly_chart(fig_cm, use_container_width=True)

    # =====================================================
    # CONFUSION METRICS (STATIC CALCULATION)
    # =====================================================
    TN, FP, FN, TP = cm.ravel()
    total = cm.sum()

    accuracy = (TP + TN) / total
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1_score = 2 * (precision * recall) / (precision + recall)

    # =====================================================
    # METRICS + RADAR (SIDE BY SIDE)
    # =====================================================
    col_left, col_right = st.columns([1, 1])

    # ---------------- METRICS ----------------
    with col_left:
        st.markdown("### 📈 Performance Metrics")

        c1, c2 = st.columns(2)
        c1.metric("Accuracy", f"{accuracy*100:.1f}%")
        c2.metric("Precision", f"{precision*100:.1f}%")

        c3, c4 = st.columns(2)
        c3.metric("Recall", f"{recall*100:.1f}%")
        c4.metric("F1-Score", f"{f1_score*100:.1f}%")

        metric_df = pd.DataFrame({
            "Metric": ["Accuracy", "Precision", "Recall", "F1-Score"],
            "Score": [
                accuracy * 100,
                precision * 100,
                recall * 100,
                f1_score * 100
            ]
        })

        fig_bar = px.bar(
            metric_df,
            x="Metric",
            y="Score",
            text=metric_df["Score"].round(1),
            height=260,
            color_discrete_sequence=["#dc2626"]
        )

        fig_bar.update_traces(textposition="outside")
        fig_bar.update_layout(
            yaxis_title="Percentage (%)",
            xaxis_title="",
            margin=dict(t=20, b=10)
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    # ---------------- RADAR CHART ----------------
    with col_right:
        st.markdown("### 📡 Model Balance (Radar Chart)")

        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=[
                accuracy * 100,
                precision * 100,
                recall * 100,
                f1_score * 100
            ],
            theta=["Accuracy", "Precision", "Recall", "F1-Score"],
            fill="toself",
            name="XGBoost",
            line_color="#dc2626"
        ))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(range=[60, 100])),
            height=350,
            margin=dict(t=30, b=10),
            showlegend=False
        )

        st.plotly_chart(fig_radar, use_container_width=True)

    # =========================================================
    # METRICS BAR CHART (SIDE BY SIDE, RED)
    # =========================================================
    metric_df = pd.DataFrame({
        "Metric": ["Accuracy", "Precision", "Recall", "F1-Score"],
        "Score": [
            accuracy * 100,
            precision * 100,
            recall * 100,
            f1_score * 100
        ]
    })

    fig_metric_bar = px.bar(
        metric_df,
        x="Metric",
        y="Score",
        text=metric_df["Score"].round(1),
        height=260,
        color_discrete_sequence=["#dc2626"]
    )

    fig_metric_bar.update_traces(textposition="outside")
    fig_metric_bar.update_layout(
        yaxis_title="Percentage (%)",
        xaxis_title="",
        margin=dict(t=20, b=10)
    )

    st.plotly_chart(fig_metric_bar, use_container_width=True)

    # =========================================================
    # METRICS TABLE
    # =========================================================
    st.markdown("### 📋 Detailed Model Metrics")
    st.dataframe(df_models, use_container_width=True, hide_index=True)

    st.success(
        "✅ The final XGBoost model demonstrates strong predictive performance with "
        "high accuracy and a well-balanced precision–recall tradeoff, suitable for "
        "cardiovascular disease prediction."
    )


# --------------------------------------------------
# RISK PREDICTOR + PDF
# --------------------------------------------------
with tabs[6]:
    import pickle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    import datetime, os
    import numpy as np
    import streamlit as st

    # Load trained model
    model = pickle.load(open("heart_model.pkl", "rb"))

    # ---------------- CSS for UI ----------------
    st.markdown("""
    <style>
    h1 { font-weight: 800; color: #ef4444; }
    .risk-ring { width: 160px; height: 160px; border-radius: 50%; border: 12px solid; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 800; margin: 20px auto; }
    .status { font-size: 16px; font-weight: 700; padding: 6px 20px; border-radius: 30px; color: white; display: inline-block; }
    .stButton > button { width: 100%; padding: 14px; font-size: 16px; font-weight: 700; border-radius: 12px; background-color: #2563eb; color: white; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>🫀 Cardiovascular Risk Predictor & PDF Report</h1>", unsafe_allow_html=True)
    st.caption("AI-Based Clinical Decision Support System")

    left, right = st.columns([2, 1])

    # ---------------- Input Form ----------------
    with left:
        name = st.text_input("Patient Name")
        age = st.number_input("Age", 0, 120, 40)
        gender = st.selectbox("Gender", [0,1], format_func=lambda x: "Female" if x==0 else "Male")
        height = st.number_input("Height (cm)", 50, 250, 170)
        weight = st.number_input("Weight (kg)", 20, 200, 75)
        ap_hi = st.number_input("Systolic BP", 50, 250, 130)
        ap_lo = st.number_input("Diastolic BP", 30, 200, 85)
        cholesterol = st.selectbox("Cholesterol", [1,2,3], format_func=lambda x: ["Normal","Above Normal","High"][x-1])
        gluc = st.selectbox("Glucose", [1,2,3], format_func=lambda x: ["Normal","Above Normal","High"][x-1])
        smoke = st.selectbox("🚬 Smoking", [0,1], format_func=lambda x: ["No","Yes"][x])
        alco = st.selectbox("🍷 Alcohol", [0,1], format_func=lambda x: ["No","Yes"][x])
        active = st.selectbox("💪 Physical Activity", [0,1], format_func=lambda x: ["Active","Inactive"][x])
        bmi = weight / ((height/100)**2)

        # Prediction button
        if st.button("💓 Run Prediction"):
            X = np.array([[age, gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active, bmi]])
            pred = model.predict(X)[0]
            prob = model.predict_proba(X)[0][1] * 100
            st.session_state["pred"] = pred
            st.session_state["prob"] = prob
            st.success("✅ Prediction completed!")

    # ---------------- Prediction Output ----------------
    with right:
        st.markdown("<div class='section-title'>📊 Prediction Result</div>", unsafe_allow_html=True)
        pred = st.session_state.get("pred")
        prob = st.session_state.get("prob", 0)
        if pred is None:
            st.info("Enter patient data and click 'Run Prediction'")
        else:
            color = "#dc2626" if pred==1 else "#16a34a"
            status = "HIGH RISK 🔴" if pred==1 else "LOW RISK 🟢"
            st.markdown(f"<div class='risk-ring' style='border-color:{color};color:{color}'>{int(prob)}%</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='status' style='background:{color}'>{status}</div>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("### 🩺 Clinical Advice")
            if pred==1:
                st.error(
                    "- Immediate medical consultation 🏥\n"
                    "- Control BP, cholesterol & glucose 📉\n"
                    "- Stop smoking & alcohol 🚭🍷, exercise regularly 🏃"
                )
            else:
                st.success(
                    "- Maintain healthy lifestyle 🥗🏃\n"
                    "- Balanced diet & exercise 💪\n"
                    "- Routine health checkups 🩺"
                )
            st.caption("Model Accuracy: 86%")

            if st.button("📄 Generate & Download PDF Report") and st.session_state.get("pred") is not None:
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.pagesizes import A4
                from reportlab.lib import colors
                from reportlab.lib.units import inch
                import datetime, os

                file = f"CardioSense_{name.replace(' ','_')}_Report.pdf"
                doc = SimpleDocTemplate(file, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
                styles = getSampleStyleSheet()
                story = []

                # ---------------- Custom Styles ----------------
                title_style = ParagraphStyle("TitleBlue", parent=styles["Title"], textColor=colors.HexColor("#2563eb"), spaceAfter=20)
                section_style = ParagraphStyle("SectionBlue", parent=styles["Heading2"], textColor=colors.HexColor("#2563eb"), spaceAfter=12)
                label_style = ParagraphStyle("Label", parent=styles["Normal"], fontSize=11, spaceAfter=6)
                italic_style = ParagraphStyle("Italic", parent=styles["Italic"], fontSize=10, spaceAfter=10)
                risk_color = colors.HexColor("#dc2626" if st.session_state['pred']==1 else "#16a34a")

                # ---------------- Header ----------------
                story.append(Paragraph("<b>CARDIOSENSE – CARDIOVASCULAR RISK REPORT</b>", title_style))
                story.append(Paragraph(f"Date: {datetime.datetime.now().strftime('%d-%m-%Y')}", label_style))
                story.append(Spacer(1, 12))

                # ---------------- Patient Details ----------------
                story.append(Paragraph("<b>Patient Details</b>", section_style))
                story.append(Paragraph(f"Name: {name}", label_style))
                story.append(Paragraph(f"Age: {age} years", label_style))
                story.append(Paragraph(f"Gender: {'Female' if gender==0 else 'Male'}", label_style))
                story.append(Paragraph(f"Height: {height} cm", label_style))
                story.append(Paragraph(f"Weight: {weight} kg", label_style))
                story.append(Paragraph(f"BMI: {bmi:.2f}", label_style))
                story.append(Spacer(1, 12))

                # ---------------- Clinical Parameters ----------------
                story.append(Paragraph("<b>Clinical Parameters</b>", section_style))
                story.append(Paragraph(f"Systolic BP: {ap_hi} mmHg", label_style))
                story.append(Paragraph(f"Diastolic BP: {ap_lo} mmHg", label_style))
                story.append(Paragraph(f"Cholesterol: {['Normal','Above Normal','High'][cholesterol-1]}", label_style))
                story.append(Paragraph(f"Glucose: {['Normal','Above Normal','High'][gluc-1]}", label_style))
                story.append(Paragraph(f"Smoking: {'Yes' if smoke==1 else 'No'}", label_style))
                story.append(Paragraph(f"Alcohol: {'Yes' if alco==1 else 'No'}", label_style))
                story.append(Paragraph(f"Physical Activity: {'Active' if active==1 else 'Inactive'}", label_style))
                story.append(Spacer(1, 12))

                # ---------------- Risk Assessment ----------------
                story.append(Paragraph("<b>Risk Assessment</b>", section_style))
                story.append(Paragraph(f"Predicted Risk: {'HIGH RISK 🔴' if st.session_state['pred']==1 else 'LOW RISK 🟢'}", ParagraphStyle("RiskLabel", parent=label_style, textColor=risk_color, fontSize=12)))
                story.append(Paragraph(f"Probability: {st.session_state['prob']:.2f}%", label_style))
                story.append(Spacer(1, 12))

                # ---------------- Notes ----------------
                story.append(Paragraph(
                    "⚠️ Note: This report is generated by an AI model for educational purposes only. "
                    "It is not a substitute for professional medical advice.", italic_style))
                story.append(Paragraph("Developed by: Shruti (23010101311)", label_style))

                # ---------------- Build PDF ----------------
                doc.build(story)

                with open(file, "rb") as f:
                    st.download_button("⬇️ Download PDF Report", f, file_name=file, mime="application/pdf")
                os.remove(file)


# --------------------------------------------------
# RESEARCHER INFO (outside of tabs)
# --------------------------------------------------
with tabs[7]:
    st.markdown("<div class='glass'><h2>👤 Researcher Information</h2></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='glass' style='text-align:center;'>
        <h3>Project Developer</h3>
        <h1>Shruti</h1>
        <p>ID: 23010101311</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='glass'>
            <h3>📚 Project Details</h3>
            <p><strong>Project Name:</strong> CardioSense AI</p>
            <p><strong>Course:</strong> Machine Learning & Deep Learning</p>
            <p><strong>Course Code:</strong> 2301CS621</p>
            <p><strong>Application Type:</strong> Cardiovascular Risk Assessment System</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='glass'>
            <h3>🔬 Technical Stack</h3>
            <p><strong>Framework:</strong> Streamlit</p>
            <p><strong>Machine Learning:</strong> Scikit-learn, XGBoost</p>
            <p><strong>Visualization:</strong> Plotly</p>
            <p><strong>Report Generation:</strong> ReportLab / FPDF</p>
            <p><strong>Data Processing:</strong> Pandas, NumPy</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='glass'><small>© 2025 CardioSense | Machine Learning Project | 2301CS621</small></div>", unsafe_allow_html=True)
