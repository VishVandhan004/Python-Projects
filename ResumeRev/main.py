import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to generate response from Gemini
def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # ✅ valid model
    response = model.generate_content(prompt)
    return response.text

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Streamlit UI
st.title("📄 ATS Insight: AI-Powered Resume Evaluator")
st.markdown("Boost your resume with **AI-Powered Evaluation**")

jd = st.text_area("📌 Paste the Job Description")
uploaded_file = st.file_uploader("🔗 Upload Your Resume (PDF only)", type="pdf")

submit = st.button("🚀 Submit for Evaluation")

# On Submit
if submit:
    if uploaded_file is not None and jd.strip() != "":
        resume_text = input_pdf_text(uploaded_file)

        # Combined and structured prompt
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
            response = get_gemini_response(filled_prompt)

            # Display results
            st.subheader("📊 AI Evaluation Report")
            
            # Extract JD Match % from the response to show a progress bar
            import re
            match = re.search(r"JD Match\s*[:\-–]?\s*(\d+)%", response)
            if match:
                match_percent = int(match.group(1))
                st.markdown("**📈 ATS Match Score**")
                st.progress(match_percent / 100)
                st.markdown(f"**Match Percentage:** {match_percent}%")

            st.markdown("---")
            st.markdown(response)

        except Exception as e:
            st.error(f"❌ Something went wrong: {str(e)}")
    else:
        st.warning("⚠️ Please provide both a Job Description and a Resume.")
