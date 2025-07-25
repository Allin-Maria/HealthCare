import streamlit as st
import pandas as pd


# ✅ Load trained model
try:
    model = joblib.load("ckd_rf_model.joblib")
except Exception as e:
    st.error("❌ Failed to load model: " + str(e))
    st.stop()

# ✅ App Title
st.title("🔬 CKD Risk Predictor")
st.markdown("This app predicts the risk of **Chronic Kidney Disease (Stage 3B or worse)** based on health records.")

# ✅ Input fields (Sidebar)
st.sidebar.header("Enter Patient Information:")

sex = st.sidebar.selectbox("Sex", [0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
age = st.sidebar.slider("Age", 18, 100, 50)
diabetes = st.sidebar.selectbox("History of Diabetes", [0, 1])
chd = st.sidebar.selectbox("History of Coronary Heart Disease", [0, 1])
vascular = st.sidebar.selectbox("History of Vascular Disease", [0, 1])
smoking = st.sidebar.selectbox("History of Smoking", [0, 1])
htn = st.sidebar.selectbox("History of Hypertension", [0, 1])
dld = st.sidebar.selectbox("History of Dyslipidemia", [0, 1])
obesity = st.sidebar.selectbox("History of Obesity", [0, 1])
dldmeds = st.sidebar.selectbox("DLD Medications", [0, 1])
dmmeds = st.sidebar.selectbox("Diabetes Medications", [0, 1])
htnmeds = st.sidebar.selectbox("Hypertension Medications", [0, 1])
aceiarb = st.sidebar.selectbox("ACEI/ARB Usage", [0, 1])
chol = st.sidebar.number_input("Cholesterol Baseline (mmol/L)", 2.0, 10.0, 5.0)
creatinine = st.sidebar.number_input("Creatinine Baseline (µmol/L)", 20.0, 300.0, 70.0)
egfr = st.sidebar.number_input("eGFR Baseline (mL/min/1.73m²)", 15.0, 120.0, 90.0)
sbp = st.sidebar.slider("Systolic BP (mmHg)", 80, 200, 130)
dbp = st.sidebar.slider("Diastolic BP (mmHg)", 40, 120, 80)
bmi = st.sidebar.number_input("BMI", 10.0, 50.0, 25.0)
time_to_event = st.sidebar.slider("Time to Event (Months)", 0, 120, 60)

# ✅ When Predict button is clicked
if st.sidebar.button("🔍 Predict Risk"):

    # ✅ Prepare input as DataFrame
    input_data = pd.DataFrame([[
        sex, age, diabetes, chd, vascular, smoking, htn, dld, obesity,
        dldmeds, dmmeds, htnmeds, aceiarb, chol, creatinine,
        egfr, sbp, dbp, bmi, time_to_event
    ]], columns=[
        'Sex', 'AgeBaseline', 'HistoryDiabetes', 'HistoryCHD', 'HistoryVascular',
        'HistorySmoking', 'HistoryHTN ', 'HistoryDLD', 'HistoryObesity',
        'DLDmeds', 'DMmeds', 'HTNmeds', 'ACEIARB', 'CholesterolBaseline',
        'CreatinineBaseline', 'eGFRBaseline', 'sBPBaseline', 'dBPBaseline',
        'BMIBaseline', 'TimeToEventMonths'
    ])

    # ✅ Predict label and probability
    try:
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

        # ✅ Display result
        st.subheader("📊 Prediction Result")
        if prediction == 1:
            st.error(f"⚠️ High Risk of CKD\n\n**Probability: {probability:.2%}**")
        else:
            st.success(f"✅ Low Risk of CKD\n\n**Probability: {probability:.2%}**")

    except Exception as e:
        st.error(f"❌ Prediction failed: {str(e)}")
