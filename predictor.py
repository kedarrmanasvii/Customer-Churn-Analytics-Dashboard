"""Churn Predictor page: loads final_churn_model.joblib and scores one customer."""
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "final_churn_model.joblib"


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


def render():
    st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0B1220 0%, #111D32 55%, #172640 100%);
        color: #F1F5F9;
    }

    /* Main content width and spacing */
    .block-container {
        max-width: 1250px;
        padding-top: 2.2rem;
        padding-bottom: 2rem;
    }

    /* Typography */
    h1, h2, h3 {
        color: #F8FAFC !important;
        letter-spacing: -0.4px;
    }
    p, label, .stMarkdown, .stCaption {
        color: #C6D2E2;
    }
    [data-testid="stCaptionContainer"] {
        color: #9BAEC8 !important;
    }

    /* Header */
    .hero {
        background: linear-gradient(120deg, #1D3151, #17243A);
        border: 1px solid #304663;
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 25px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.16);
    }
    .hero-label {
        color: #8DBBFF;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .hero-title {
        color: #FFFFFF;
        font-size: 2.15rem;
        font-weight: 750;
        margin: 8px 0;
    }
    .hero-subtitle {
        color: #B8C8DD;
        font-size: 1rem;
        line-height: 1.6;
    }
    .model-pill {
        display: inline-block;
        background: #243D5E;
        color: #A9D0FF;
        border: 1px solid #3B5D84;
        padding: 6px 12px;
        border-radius: 30px;
        font-size: 0.8rem;
        margin-top: 12px;
    }

    /* Form panel */
    [data-testid="stForm"] {
        background: #142238;
        border: 1px solid #2A3F5D;
        border-radius: 18px;
        padding: 24px;
    }

    /* Section headings */
    .section-heading {
        font-size: 1.16rem;
        font-weight: 700;
        color: #F1F6FF;
        padding-bottom: 10px;
        margin: 10px 0 18px 0;
        border-bottom: 1px solid #30435F;
    }

    /* Input labels */
    [data-testid="stWidgetLabel"] p {
        color: #D8E3F1 !important;
        font-weight: 500;
    }

    /* Inputs and select boxes */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"] {
        background-color: #1C2D45 !important;
        border: 1px solid #3B506C !important;
        border-radius: 9px !important;
    }
    div[data-baseweb="select"] *,
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input {
        color: #F1F5F9 !important;
    }
    div[data-baseweb="select"] svg {
        fill: #BBD0EB !important;
    }
    [data-testid="stNumberInput"] button {
        background: #263D5B !important;
        color: white !important;
        border-color: #3B506C !important;
    }

    /* Buttons */
    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(90deg, #3679E8, #4D91FA) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1rem !important;
        font-weight: 700 !important;
        min-height: 48px;
        transition: 0.2s ease;
    }
    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(90deg, #2866D0, #3A7FEA) !important;
        box-shadow: 0 5px 18px rgba(55, 125, 235, 0.28);
        transform: translateY(-1px);
    }

    /* Result cards */
    .result-card {
        background: linear-gradient(145deg, #1B2C43, #16253A);
        border: 1px solid #304863;
        border-radius: 16px;
        padding: 22px;
        min-height: 145px;
    }
    .result-label {
        color: #AFC1D8;
        font-size: 0.85rem;
        margin-bottom: 12px;
    }
    .result-value {
        color: #FFFFFF;
        font-size: 1.7rem;
        font-weight: 750;
    }
    .result-note {
        color: #AFC1D8;
        font-size: 0.82rem;
        margin-top: 7px;
    }

    /* Alerts */
    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid #344B69;
    }

    /* Progress bar */
    [data-testid="stProgressBar"] > div {
        background-color: #2A3D57;
        border-radius: 20px;
    }
    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #4387F5, #73B3FF);
        border-radius: 20px;
    }

    /* Data table and expander */
    [data-testid="stDataFrame"] {
        border: 1px solid #344963;
        border-radius: 10px;
    }
    [data-testid="stExpander"] {
        background: #16263B;
        border: 1px solid #30445F;
        border-radius: 12px;
    }

    /* Dividers and footer */
    hr {
        border-color: #30435B !important;
    }
    .footer {
        text-align: center;
        color: #8297B4;
        font-size: 0.82rem;
        padding-top: 10px;
    }

    /* Mobile adjustments */
    @media (max-width: 700px) {
        .hero {
            padding: 22px 18px;
        }
        .hero-title {
            font-size: 1.65rem;
        }
        [data-testid="stForm"] {
            padding: 15px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    try:
        model = load_model()
    except Exception as e:
        st.error("Could not load the trained model.")
        st.write(
            "Check that final_churn_model.joblib is in the same folder as app.py."
        )
        st.exception(e)
        st.stop()

    # =====================================================
    # HERO HEADER
    # =====================================================
    st.markdown("""
    <div class="hero">
        <div class="hero-label">CUSTOMER INTELLIGENCE · ML PROJECT</div>
        <div class="hero-title">Customer Churn Analytics</div>
        <div class="hero-subtitle">
            Identify customers at risk of leaving and support smarter
            customer-retention decisions using machine learning.
        </div>
        <div class="model-pill">● Gradient Boosting Model</div>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # CUSTOMER INPUT FORM
    # =====================================================
    st.markdown(
        '<div class="section-heading">👤 &nbsp; Customer Information</div>',
        unsafe_allow_html=True
    )

    with st.form("customer_form"):
        st.markdown("##### Personal and Account Details")

        col1, col2, col3 = st.columns(3)

        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"])
            senior_citizen = st.selectbox(
                "Senior Citizen", [0, 1],
                format_func=lambda x: "Yes" if x == 1 else "No"
            )
            partner = st.selectbox("Has Partner?", ["Yes", "No"])

        with col2:
            dependents = st.selectbox("Has Dependents?", ["Yes", "No"])
            tenure = st.number_input(
                "Tenure (Months)", min_value=0, max_value=72, value=12
            )
            phone_service = st.selectbox("Phone Service", ["Yes", "No"])

        with col3:
            multiple_lines = st.selectbox(
                "Multiple Lines", ["No", "Yes", "No phone service"]
            )
            internet_service = st.selectbox(
                "Internet Service", ["DSL", "Fiber optic", "No"]
            )
            contract = st.selectbox(
                "Contract Type",
                ["Month-to-month", "One year", "Two year"]
            )

        paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])

        st.markdown("---")
        st.markdown("##### 📡 Online Services")

        col4, col5, col6 = st.columns(3)

        with col4:
            online_security = st.selectbox(
                "Online Security", ["No", "Yes", "No internet service"]
            )
            online_backup = st.selectbox(
                "Online Backup", ["No", "Yes", "No internet service"]
            )

        with col5:
            device_protection = st.selectbox(
                "Device Protection", ["No", "Yes", "No internet service"]
            )
            tech_support = st.selectbox(
                "Tech Support", ["No", "Yes", "No internet service"]
            )

        with col6:
            streaming_tv = st.selectbox(
                "Streaming TV", ["No", "Yes", "No internet service"]
            )
            streaming_movies = st.selectbox(
                "Streaming Movies", ["No", "Yes", "No internet service"]
            )

        st.markdown("---")
        st.markdown("##### 💳 Billing Details")

        col7, col8, col9 = st.columns(3)

        with col7:
            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer (automatic)",
                    "Credit card (automatic)"
                ]
            )

        with col8:
            monthly_charges = st.number_input(
                "Monthly Charges", min_value=0.0, value=70.0, step=1.0
            )

        with col9:
            total_charges = st.number_input(
                "Total Charges", min_value=0.0, value=1500.0, step=10.0
            )

        submitted = st.form_submit_button(
            "🔍  Predict Customer Churn", use_container_width=True
        )

    # =====================================================
    # PREDICTION
    # =====================================================
    if submitted:
        # Match service values to dataset conventions
        if phone_service == "No":
            multiple_lines = "No phone service"

        if internet_service == "No":
            online_security = "No internet service"
            online_backup = "No internet service"
            device_protection = "No internet service"
            tech_support = "No internet service"
            streaming_tv = "No internet service"
            streaming_movies = "No internet service"

        input_dict = {
            "gender": gender,
            "SeniorCitizen": senior_citizen,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone_service,
            "MultipleLines": multiple_lines,
            "InternetService": internet_service,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "Contract": contract,
            "PaperlessBilling": paperless_billing,
            "PaymentMethod": payment_method,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges
        }

        input_df = pd.DataFrame([input_dict])

        try:
            prediction = int(model.predict(input_df)[0])
            probabilities = model.predict_proba(input_df)[0]
            classes = list(model.classes_)
            churn_index = classes.index(1)
            churn_probability = float(probabilities[churn_index])

            st.markdown("---")
            st.markdown(
                '<div class="section-heading">📈 &nbsp; Prediction Results</div>',
                unsafe_allow_html=True
            )

            if prediction == 1:
                result_text = "LIKELY TO CHURN"
                result_colour = "#FF8585"
                result_note = "Customer may be at risk of leaving."
                action_text = (
                    "Review the customer's contract, service experience, "
                    "and billing concerns."
                )
            else:
                result_text = "LIKELY TO STAY"
                result_colour = "#65D6A2"
                result_note = "Customer is predicted to remain."
                action_text = (
                    "Continue providing good service and monitor "
                    "the customer's experience."
                )

            if churn_probability < 0.30:
                risk_level = "LOW"
                risk_note = "Lower estimated churn risk"
                risk_colour = "#65D6A2"
            elif churn_probability < 0.60:
                risk_level = "MEDIUM"
                risk_note = "Moderate estimated churn risk"
                risk_colour = "#F7C66A"
            else:
                risk_level = "HIGH"
                risk_note = "Higher estimated churn risk"
                risk_colour = "#FF8585"

            result_col, probability_col, risk_col = st.columns(3)

            with result_col:
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-label">Prediction</div>
                    <div class="result-value" style="color:{result_colour}">
                        {result_text}
                    </div>
                    <div class="result-note">{result_note}</div>
                </div>
                """, unsafe_allow_html=True)

            with probability_col:
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-label">Churn Probability</div>
                    <div class="result-value">{churn_probability:.1%}</div>
                    <div class="result-note">Model-estimated probability</div>
                </div>
                """, unsafe_allow_html=True)

            with risk_col:
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-label">Risk Level</div>
                    <div class="result-value" style="color:{risk_colour}">
                        {risk_level}
                    </div>
                    <div class="result-note">{risk_note}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("##### Churn Probability Indicator")
            st.progress(min(max(churn_probability, 0.0), 1.0))

            st.markdown("##### 💡 Suggested Next Step")
            st.info(action_text)

            with st.expander("View submitted customer details"):
                st.dataframe(input_df, use_container_width=True)

        except Exception as e:
            st.error(
                "Prediction failed. Check that the model uses the same "
                "19 input features and original column names."
            )
            st.exception(e)

    # =====================================================
    # FOOTER
    # =====================================================
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        CUSTOMER CHURN ANALYTICS &nbsp; · &nbsp; GRADIENT BOOSTING
        <br>
        Machine Learning + Power BI Project
    </div>
    """, unsafe_allow_html=True)
