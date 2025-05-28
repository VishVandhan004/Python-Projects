import streamlit as st
import joblib

# Load trained model
model = joblib.load("symptom_disease_model.pkl")

# App title
st.title("🩺 Smart Health Symptom Checker")

# Input field
symptoms = st.text_area("Enter your symptoms (comma separated):")

# Predict button
if st.button("Check Condition"):
    if not symptoms.strip():
        st.warning("Please enter symptoms.")
    else:
        prediction = model.predict([symptoms])[0]
        st.success(f"Predicted Disease Label: {prediction}")
