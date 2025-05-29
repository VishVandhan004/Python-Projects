from datetime import datetime  # Import datetime module to work with timestamps
import base64                  # Import base64 for encoding PDF content to base64 string for download links
from fpdf import FPDF          # Import FPDF library to generate PDF reports
import re                      # Import regex module for cleaning text
import requests                # Import requests to make HTTP requests for geolocation and hospital data

def get_specialist(symptoms: str) -> str:
    # Maps common symptoms keywords to medical specialists
    mapping = {
        "fever": "General Physician",
        "headache": "Neurologist",
        "chest pain": "Cardiologist",
        "skin rash": "Dermatologist",
        "anxiety": "Psychiatrist"
    }
    # Check if any keyword exists in symptoms (case-insensitive) and return corresponding specialist
    for keyword in mapping:
        if keyword in symptoms.lower():
            return mapping[keyword]
    # Default specialist if no keyword matched
    return "General Physician"

def get_risk_level(symptoms: str) -> str:
    # Maps certain keywords to risk levels with emoji indicators
    risk_keywords = {
        "severe": "🔴 High Risk",
        "chest pain": "🔴 High Risk",
        "difficulty breathing": "🔴 High Risk",
        "moderate": "🟠 Medium Risk",
        "mild": "🟢 Low Risk",
        "headache": "🟢 Low Risk"
    }
    # Check for any keyword in symptoms and return corresponding risk level
    for keyword, risk in risk_keywords.items():
        if keyword in symptoms.lower():
            return risk
    # Default low risk if no keyword matched
    return "🟢 Low Risk"

def clean_text(text):
    # Remove emojis and non-ASCII characters to avoid PDF encoding issues
    return re.sub(r'[^\x00-\x7F]+', '', text)

def export_to_pdf(symptoms, conditions, specialist, risk_level, tips):
    # Create PDF report summarizing symptom analysis
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title centered on the page
    pdf.cell(200, 10, txt="MediMentor AI - Symptom Report", ln=1, align="C")
    pdf.ln(10)  # Line break

    # Add report content with date/time and cleaned text to avoid encoding problems
    pdf.multi_cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    pdf.multi_cell(0, 10, f"Symptoms: {clean_text(symptoms)}")
    pdf.multi_cell(0, 10, f"Conditions: {clean_text(conditions)}")
    pdf.multi_cell(0, 10, f"Specialist: {clean_text(specialist)}")
    pdf.multi_cell(0, 10, f"Risk Level: {clean_text(risk_level)}")
    pdf.multi_cell(0, 10, f"Health Tips: {clean_text(tips)}")

    filename = "medimentor_report.pdf"
    pdf.output(filename)  # Save PDF to file

    # Read saved PDF and encode to base64 for embedding in HTML download link
    with open(filename, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        # Create clickable HTML link for downloading the PDF report
        href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="{filename}">📥 Download Symptom Report</a>'
        return href

# Dictionary mapping symptoms to lists of suggested medicines
medicine_suggestions = {
    "fever": ["Paracetamol", "Ibuprofen"],
    "headache": ["Aspirin", "Ibuprofen"],
    "cough": ["Dextromethorphan", "Guaifenesin"],
    "sore throat": ["Lozenges", "Ibuprofen"],
    "allergy": ["Loratadine", "Cetirizine"],
    "chest pain": ["Nitroglycerin"],  # urgent attention needed
    "anxiety": ["Diazepam", "Lorazepam"],  # use cautiously
}

def suggest_medicines(symptoms: str) -> list:
    # Analyze symptoms string to suggest relevant medicines
    suggestions = []
    for symptom, meds in medicine_suggestions.items():
        if symptom in symptoms.lower():
            suggestions.extend(meds)
    # Remove duplicates by converting to set then back to list
    return list(set(suggestions))

def medicine_info_links(medicines: list) -> list:
    # Generate markdown-style clickable links to drugs.com search results for each medicine
    base_url = "https://www.drugs.com/search.php?searchterm="
    links = []
    for med in medicines:
        # Replace spaces with '+' for URL query parameter
        link = f"[{med}]({base_url}{med.replace(' ', '+')})"
        links.append(link)
    return links

def get_lat_lng_from_pincode_nominatim(pincode, country='India'):
    # Use OpenStreetMap Nominatim API to get latitude and longitude for a given postal code and country
    url = f"https://nominatim.openstreetmap.org/search?postalcode={pincode}&country={country}&format=json"
    response = requests.get(url, headers={'User-Agent': 'MediMentorAI/1.0'})
    data = response.json()
    if data:
        # Return first result's lat and lon as floats
        return float(data[0]['lat']), float(data[0]['lon'])
    else:
        # Raise error if no location found for given pincode
        raise ValueError("Invalid pincode or no location found")

def get_hospitals_nearby_overpass(lat, lon, radius=5000):
    # Query Overpass API to find hospitals within specified radius (in meters) around given lat/lon
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      way["amenity"="hospital"](around:{radius},{lat},{lon});
      relation["amenity"="hospital"](around:{radius},{lat},{lon});
    );
    out center 10;
    """
    response = requests.get(overpass_url, params={'data': query})
    data = response.json()
    hospitals = []
    # Extract hospital names and optional addresses from response elements
    for element in data.get('elements', []):
        name = element.get('tags', {}).get('name', 'Unnamed Hospital')
        addr = element.get('tags', {}).get('addr:full', '') or element.get('tags', {}).get('address', '')
        hospitals.append(name + (f" — {addr}" if addr else ""))
        # Limit to 5 hospitals maximum
        if len(hospitals) >= 5:
            break
    return hospitals
