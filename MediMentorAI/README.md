# MediMentor AI – Your Health Companion

![MediMentor AI]  
*Your AI-powered personal health assistant.*

---

## Project Overview

**MediMentor AI** is an AI-powered health assistant web application built with Streamlit. It helps users analyze their symptoms, get probable health conditions, receive specialist recommendations, find nearby hospitals, learn about medicines, and export their health reports — all from an easy-to-use interface.

Powered by Gemini AI and open geolocation data, MediMentor AI aims to be your go-to digital health companion for quick and informative health insights.

---

## Live Demo

Access the deployed app here:  
👉 [https://vishnus-medimentor-ai.streamlit.app/](https://vishnus-medimentor-ai.streamlit.app/)

---

## Features

- **Symptom Checker:**  
  Enter symptoms to get AI-generated probable conditions, recommended specialists, risk levels, and helpful health tips.

- **Medicine Information:**  
  Search for medicines to receive detailed information and usage tips.

- **Nearby Hospitals Finder:**  
  Enter your postal pincode to locate hospitals near your area using OpenStreetMap data.

- **Symptom History:**  
  Your past symptom analyses are saved locally for reference.

- **Export to PDF:**  
  Generate and download a comprehensive PDF report of your symptom analysis.

---

## Tech Stack & Libraries

- **Python 3.8+**
- **Streamlit:** Web interface
- **Gemini AI API:** AI-powered health insights
- **SQLite3:** Local database for symptom history
- **Geopy:** Geocoding pincode to coordinates using OpenStreetMap Nominatim
- **Overpass API:** Querying nearby hospitals from OpenStreetMap
- **FPDF / ReportLab (or similar):** PDF report generation
- **Requests, Pandas:** HTTP requests and data handling

---

## Project Structure

```
/medimentor-ai
│
├── app.py                  # Main Streamlit app
├── gemini.py               # Gemini AI API integrations
├── utils.py                # Helper functions (DB, geolocation, hospital search, PDF export)
├── database.py             # SQLite3 DB connection and schema
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## Installation & Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/medimentor-ai.git
   cd medimentor-ai
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your Gemini AI API credentials inside `gemini.py` as needed.

5. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

6. Open the URL displayed by Streamlit (usually http://localhost:8501) in your browser.

---

## Usage

- Enter your symptoms in the text area.
- Optionally, enter a postal pincode to get nearby hospital suggestions.
- Click **Analyze** to get your health insights.
- Use the sidebar to search for medicine information.
- Export your report to PDF for sharing or printing.
- Your symptom history will be saved in the local SQLite database.

---

## APIs & Services Used

- **Gemini AI API:** For AI-powered symptom analysis, health tips, and medicine info.
- **OpenStreetMap Nominatim (via Geopy):** Converts pincode to latitude and longitude.
- **OpenStreetMap Overpass API:** Finds hospitals near the coordinates.
- **SQLite:** Stores symptom history locally.
- **Streamlit:** User interface and web app framework.

---

## Future Improvements

- Add multi-language support and real-time translation.
- Voice input for symptom descriptions.
- Machine learning-based risk prediction.
- User authentication and cloud-based data storage.
- Appointment booking and emergency contact features.
- Enhanced UI/UX and mobile responsiveness.

---

## Disclaimer

**MediMentor AI** is designed for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a licensed healthcare provider for medical concerns.

---

## Contact

For questions, suggestions, or contributions, please contact:

- **Vishnu Vandhan**    
- GitHub: [VishVandhan004](https://github.com/VishVandhan004)

---

Thank you for using **MediMentor AI – Your Health Companion**!  
Built with ❤️ using Gemini AI & Streamlit.
