import streamlit as st
from gemini import get_conditions, get_health_tips, get_medicine_info
from utils import (
    get_specialist, get_risk_level, export_to_pdf,
    suggest_medicines, medicine_info_links,
    get_lat_lng_from_pincode_nominatim, get_hospitals_nearby_overpass
)
from database import init_db, save_symptom_history  # Import functions to initialize DB and save history

# Set Streamlit page configuration: title, layout, and icon in browser tab
st.set_page_config(page_title="MediMentor AI – Your Health Companion", layout="centered", page_icon="🧠")

# Initialize the SQLite database and create tables if they don't exist
init_db()

# --- Custom CSS styling injected into the Streamlit app ---
st.markdown("""
    <style>
        .big-title {
            font-size: 2.2rem;             /* Large font size for main title */
            font-weight: bold;             /* Bold text */
            color: #0066cc;                /* Blue color */
            margin-bottom: 20px;           /* Space below the title */
        }
        .subtitle {
            font-size: 1.1rem;             /* Slightly smaller font for subtitle */
            color: #ccc;                   /* Light gray color */
            margin-bottom: 40px;           /* Space below subtitle */
        }
        .section-header {
            font-size: 1.4rem;             /* Medium-large font for section headers */
            font-weight: bold;             /* Bold text */
            margin-top: 50px;              /* Space above header */
            margin-bottom: 10px;           /* Space below header */
            color: #ccc;                   /* Light gray color */
        }
        .footer {
            margin-top: 60px;              /* Space above footer */
            font-size: 0.85rem;            /* Smaller font size */
            text-align: center;            /* Center aligned text */
            color: gray;                  /* Gray text color */
        }
        .stTextArea textarea {
            font-size: 1.1rem;             /* Custom font size for textarea input */
            line-height: 1.6;              /* Line height for readability */
        }
    </style>
""", unsafe_allow_html=True)  # Allow HTML and CSS injection safely

# --- Sidebar Section for Medicine Info Query ---
st.sidebar.header("💊 Want to know about a medicine?")  # Sidebar header text
med_name = st.sidebar.text_input("Enter medicine name (tablet, eye drop, etc.)")  # Text input for medicine name

# If user entered any medicine name (non-empty after stripping whitespace)
if med_name.strip():
    # Show a loading spinner while fetching medicine info
    with st.spinner(f"Fetching info about '{med_name}'..."):
        try:
            # Fetch medicine information using Gemini API wrapper function
            med_info = get_medicine_info(med_name.strip())
            # Display medicine info title and the fetched info in the sidebar
            st.sidebar.markdown(f"### Info for: {med_name}")
            st.sidebar.info(med_info)
        except Exception as e:
            # Show error message if fetching fails
            st.sidebar.error(f"❌ Could not fetch info: {e}")

# --- Main Page Title & Description ---
st.markdown('<div class="big-title">🧠 MediMentor AI – Your Health Companion</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">🤖 Powered by <b>Gemini AI</b> & more – Your personal health assistant.<br>'
    '💬 Check symptoms, get medicine info, and find nearby hospitals all in one place.</div>',
    unsafe_allow_html=True
)

# --- Input area for user to describe symptoms ---
symptoms = st.text_area("📝 Describe your symptoms", placeholder="e.g., fever, sore throat, headache")

# --- Input for user's pincode to suggest hospitals nearby ---
pincode = st.text_input("🏥 Enter your pincode for nearby hospital suggestions")

# --- Analyze Button ---
if st.button("🔍 Analyze"):
    # Validate that symptoms are provided (non-empty after stripping)
    if not symptoms.strip():
        st.warning("⚠️ Please enter some symptoms.")  # Warn user to input symptoms
    else:
        # Show spinner while analysis runs
        with st.spinner("🧠 MediMentor AI is analyzing your symptoms..."):
            try:
                # Use Gemini AI API to get probable conditions from symptoms
                conditions = get_conditions(symptoms)
                # Get health tips related to symptoms
                tips = get_health_tips(symptoms)
                # Get recommended medical specialist for symptoms
                specialist = get_specialist(symptoms)
                # Get risk level assessment from symptoms
                risk_level = get_risk_level(symptoms)
                
                # Save symptom analysis results into SQLite database
                save_symptom_history(symptoms, conditions, tips)

                # Display the results on the UI in separate sections with styled headers
                st.markdown('<div class="section-header">🔬 Most Probable Conditions</div>', unsafe_allow_html=True)
                st.success(conditions)  # Show probable conditions in success message box

                st.markdown('<div class="section-header">👨‍⚕️ Recommended Specialist</div>', unsafe_allow_html=True)
                st.info(specialist)  # Show recommended specialist info box

                st.markdown('<div class="section-header">🚦 Risk Level</div>', unsafe_allow_html=True)
                st.warning(risk_level)  # Show risk level with warning style

                st.markdown('<div class="section-header">💡 Helpful Health Tips</div>', unsafe_allow_html=True)
                st.info(tips)  # Show health tips in info box

                # Suggest medicines based on symptoms
                medicines = suggest_medicines(symptoms)
                if medicines:
                    st.markdown('<div class="section-header">💊 Suggested Medicines</div>', unsafe_allow_html=True)
                    # Display clickable links for medicine info
                    for med_link in medicine_info_links(medicines):
                        st.markdown(med_link)
                else:
                    # Inform if no medicine suggestions are available
                    st.info("No medicine suggestions available for the entered symptoms.")

                # Provide option to export the report as PDF and show the download link
                st.markdown('<div class="section-header">📄 Export Report</div>', unsafe_allow_html=True)
                pdf_link = export_to_pdf(symptoms, conditions, specialist, risk_level, tips)
                st.markdown(pdf_link, unsafe_allow_html=True)

                # If user entered a pincode, attempt to fetch nearby hospitals
                if pincode.strip():
                    with st.spinner(f"Fetching hospitals near {pincode}..."):
                        try:
                            # Get latitude and longitude for the pincode using Nominatim API
                            lat, lon = get_lat_lng_from_pincode_nominatim(pincode.strip())
                            # Fetch list of nearby hospitals using Overpass API
                            hospitals = get_hospitals_nearby_overpass(lat, lon)
                            if hospitals:
                                # Display list of hospitals under a styled header
                                st.markdown('<div class="section-header">🏥 Nearby Hospitals</div>', unsafe_allow_html=True)
                                for h in hospitals:
                                    st.write(f"- {h}")
                            else:
                                # Inform user if no hospitals found near the pincode
                                st.info("No hospitals found near the entered pincode.")
                        except Exception as e:
                            # Show error if hospital fetching fails
                            st.error(f"Error fetching hospitals: {e}")

            except Exception as e:
                # General error handler for the analysis process
                st.error(f"❌ Something went wrong: {e}")

# --- Footer with disclaimer and credits ---
st.markdown("""
    <div class="footer">
        🛡️ MediMentor AI is for informational purposes only. Always consult a licensed medical professional.<br>
        Built with ❤️ using Gemini AI & Streamlit.
    </div>
""", unsafe_allow_html=True)
