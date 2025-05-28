import streamlit as st
from gemini import get_conditions, get_health_tips

st.set_page_config(page_title="MediMentor AI – Symptom Checker", layout="centered", page_icon="🧠")

# --- Custom CSS ---
st.markdown("""
    <style>
        .big-title {
            font-size: 2.2rem;
            font-weight: bold;
            color: #0066cc;
            margin-bottom: 20px;
        }
        .subtitle {
            font-size: 1.1rem;
            color: #ccc;
            margin-bottom: 40px;
        }
        .section-header {
            font-size: 1.4rem;
            font-weight: bold;
            margin-top: 50px;
            margin-bottom: 10px;
            color: #ccc;
        }
        .footer {
            margin-top: 60px;
            font-size: 0.85rem;
            text-align: center;
            color: gray;
        }
        .stTextArea textarea {
            font-size: 1.1rem;
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title & Description ---
st.markdown('<div class="big-title">🧠 MediMentor AI – Symptom Checker</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">🤖 Powered by <b>Gemini AI</b> – Your personal health assistant.<br>'
            '💬 Enter your symptoms to get potential causes and self-care tips.</div>', unsafe_allow_html=True)

# --- Symptom Input ---
symptoms = st.text_area("📝 Describe your symptoms", placeholder="e.g., fever, sore throat, headache")

# --- Analyze Button ---
if st.button("🔍 Analyze"):
    if not symptoms.strip():
        st.warning("⚠️ Please enter some symptoms.")
    else:
        with st.spinner("🧠 MediMentor AI is analyzing your symptoms..."):
            try:
                conditions = get_conditions(symptoms)
                tips = get_health_tips(symptoms)

                # --- Results Section ---
                st.markdown('<div class="section-header">🔬 Most Probable Conditions</div>', unsafe_allow_html=True)
                st.success(conditions)

                st.markdown('<div class="section-header">💡 Helpful Health Tips</div>', unsafe_allow_html=True)
                st.info(tips)

            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")

# --- Footer ---
st.markdown("""
    <div class="footer">
        🛡️ MediMentor AI is for informational purposes only. Always consult a licensed medical professional.<br>
        Built with ❤️ using Gemini AI & Streamlit.
    </div>
""", unsafe_allow_html=True)
