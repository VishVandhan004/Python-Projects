# Import the Streamlit library for building interactive web apps
import streamlit as st

# Import the Google Generative AI SDK to interact with Gemini models
import google.generativeai as genai

# Provides a way to work with environment variables (e.g., loading API keys)
import os

# Used to extract text from PDF files
import PyPDF2 as pdf

# Loads environment variables from a .env file
from dotenv import load_dotenv

# Load all environment variables from .env into the environment
load_dotenv()

# Configure the Generative AI client with the Google API key from the environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to generate a response using Gemini AI based on a prompt
def get_gemini_response(prompt):
    # Initialize the Gemini model (using the 'gemini-2.0-flash' variant)
    model = genai.GenerativeModel('gemini-2.0-flash')

    # Generate a response based on the given prompt
    response = model.generate_content(prompt)

    # Return only the text part of the response
    return response.text


# Function to extract text content from an uploaded PDF file
def input_pdf_text(uploaded_file):
    # Initialize a PDF reader using the uploaded file
    reader = pdf.PdfReader(uploaded_file)

    # Initialize a string to hold the entire extracted text
    text = ""

    # Loop through each page of the PDF and extract its text
    for page in reader.pages:
        text += page.extract_text()

    # Return the combined text from all pages
    return text


# ---------- Streamlit UI Setup Below ----------

# Title of the Streamlit web app
st.title("📄 ATS Insight: AI-Powered Resume Evaluator")

# Subtitle or introduction to the app
st.markdown("Boost your resume with **AI-Powered Evaluation**")

# Text area for the user to paste the job description
jd = st.text_area("📌 Paste the Job Description")

# Upload component that allows users to upload a PDF resume
uploaded_file = st.file_uploader("🔗 Upload Your Resume (PDF only)", type="pdf")

# A button that triggers the evaluation process
submit = st.button("🚀 Submit for Evaluation")


# When the "Submit" button is clicked:
if submit:
    # Check if both a file is uploaded and job description is provided
    if uploaded_file is not None and jd.strip() != "":
        # Extract resume text from the uploaded PDF
        resume_text = input_pdf_text(uploaded_file)

        # Construct the full prompt with resume and job description for Gemini
        filled_prompt = f"""
        Act as a highly intelligent and experienced Applicant Tracking System (ATS) and resume evaluation expert.
        You specialize in analyzing technical resumes and job descriptions to provide **thorough, insightful feedback**.

        Evaluate the resume below against the job description, and give a **detailed** analysis with clear explanations and bullet points where appropriate.

        Your output must include the following sections:

        1. **ATS Score (out of 100)** – Provide an estimated ATS score based on keyword match, skill alignment, and formatting. Explain how you arrived at the score.
        2. **JD Match %** – Estimate how well the resume aligns with the job description. Consider skills, qualifications, responsibilities, and terminology.
        3. **Missing Keywords** – List important terms or phrases from the JD that are missing in the resume.
        4. **Profile Summary** – Write a professional summary of the candidate based on the resume.
        5. **Good Aspects of the Resume** – Highlight what’s working well (e.g., relevant experience, quantifiable achievements, good formatting) in a detailed way.
        6. **Bad Aspects of the Resume** – Identify shortcomings (e.g., missing technical skills, vague statements, structural issues) in a detailed way.
        7. **Areas to Improve** – Provide actionable tips to make the resume stronger and more aligned with the job description in a detailed way.
        8. **Final Verdict** – Give a conclusion: Is this resume likely to get shortlisted or rejected by an ATS? Back it up with reasons.

        Format the response in well-structured English with clear headers and bullet points. Avoid using JSON or code blocks.

        --- Resume Text ---
        {resume_text}

        --- Job Description ---
        {jd}
        """

        try:
            # Send the prompt to Gemini and get a response
            response = get_gemini_response(filled_prompt)

            # Section title for the AI-generated results
            st.subheader("📊 AI Evaluation Report")

            # Import regex module for extracting the match percentage
            import re

            # Use regex to find JD Match percentage from the response text
            match = re.search(r"JD Match\s*[:\-–]?\s*(\d+)%", response)
            if match:
                # If a percentage is found, convert it to an integer
                match_percent = int(match.group(1))

                # Display a visual progress bar for the match score
                st.markdown("**📈 ATS Match Score**")
                st.progress(match_percent / 100)
                st.markdown(f"**Match Percentage:** {match_percent}%")

            # Separator line
            st.markdown("---")

            # Display the entire formatted AI response
            st.markdown(response)

        # Handle unexpected errors during Gemini API call or response handling
        except Exception as e:
            st.error(f"❌ Something went wrong: {str(e)}")
    else:
        # Warn user if resume or job description is missing
        st.warning("⚠️ Please provide both a Job Description and a Resume.")
