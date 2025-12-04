import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

def get_conditions(symptoms):
    prompt = f"""You are a medical assistant. A user reports the following symptoms: {symptoms}.
    List the 5 most probable conditions that could be related, with a short explanation for each.
    Do not provide a diagnosis — only educational information. Also ask them to consult the doctor if they have any concerns.
"""
    response = model.generate_content(prompt)
    return response.text.strip()

def get_health_tips(symptoms):
    prompt = f"""The user is experiencing: {symptoms}.
    Provide helpful and general health tips relevant to these symptoms, such as hydration, rest, nutrition, etc.
    Avoid giving any diagnostic or emergency advice. Also remind them to consult a healthcare professional if symptoms persist or worsen.
"""
    response = model.generate_content(prompt)
    return response.text.strip()

def get_medicine_info(medicine_name):
    prompt = f"""You are a medical assistant. A user wants information about the medicine named "{medicine_name}".
    Provide a concise description about what it is used for, common dosage forms, typical side effects, and precautions.
    Do not provide any diagnosis or personalized advice. Encourage consulting a healthcare professional for more details.
"""
    response = model.generate_content(prompt)
    return response.text.strip()

