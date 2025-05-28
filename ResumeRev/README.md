## 📄 ATS Insight: AI-Powered Resume Evaluator

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20App-ff4b4b?logo=streamlit&logoColor=white)](https://vishnus-ats-insight.streamlit.app/)

ATS Insight is an intelligent resume evaluation tool that uses Google Gemini AI to assess resumes against job descriptions—providing tailored, actionable feedback to increase your chances of getting shortlisted by Applicant Tracking Systems (ATS).

---

### 🧠 Why Use ATS Insight?

Many companies use ATS software to **automatically screen resumes** before a human ever reads them. These systems look for **keyword matches**, **formatting consistency**, and **role relevance**. A well-written resume can still get rejected if it doesn’t check the right boxes algorithmically.

**ATS Insight** simulates this screening process using **advanced language models** to give you:

* An **objective evaluation** based on job description criteria
* A breakdown of **what's working well** in your resume
* A **diagnosis of missing elements** like technical keywords or qualifications
* Actionable suggestions to **enhance clarity, impact, and relevance**

---

### 🧬 How It Works Behind the Scenes

* ✅ **Text Extraction**: It reads the uploaded PDF resume using `PyPDF2`.
* 🔍 **Contextual Matching**: It compares resume content with the job description for keyword and skill overlap.
* 🤖 **AI Evaluation**: A well-crafted prompt is sent to **Gemini 1.5 Flash**, a powerful LLM, which:

  * Evaluates keyword alignment
  * Estimates ATS score
  * Suggests resume improvements
  * Writes a professional summary
* 🎯 **Feedback Delivery**: Results are rendered on the screen with match scores, suggestions, and improvement areas.

---

### 🌟 What Makes ATS Insight Special?

* **Powered by Cutting-Edge AI (Gemini)** – Get feedback based on deep understanding of language and HR patterns.
* **Real-Time Evaluation** – Immediate insights in seconds.
* **Human-Level Clarity** – Advice is detailed, readable, and designed for job seekers.
* **Zero Coding Needed** – Built on Streamlit, users just need to upload and paste.

---

## 🚀 Live Demo

👉 [Try it Now on Streamlit](https://vishnus-ats-insight.streamlit.app/)

---

## ✨ Features

- 📌 Paste any job description
- 🔗 Upload your resume as a PDF
- ⚙️ Evaluates resume using **Gemini 1.5 Flash**
- 📊 Provides:
  - ATS score (0–100)
  - JD Match percentage
  - Missing keywords
  - Resume strengths and weaknesses
  - Areas to improve
  - Final verdict on ATS success

---

## 🧠 How It Works

The app:
1. Extracts text from your PDF resume
2. Accepts job description input
3. Constructs a detailed prompt for Gemini AI
4. Analyzes the resume against the job description
5. Returns a structured and professional evaluation

---

## 🖥️ Tech Stack

| Tool/Library       | Purpose                          |
|--------------------|----------------------------------|
| [Streamlit](https://streamlit.io/)        | UI and App deployment               |
| [Google Generative AI (Gemini)](https://ai.google.dev/) | AI Resume Evaluation (LLM)         |
| [PyPDF2](https://pypi.org/project/PyPDF2/)             | Resume (PDF) text extraction        |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Environment variable management     |

---

## 📁 Project Structure
```

ResumeRev/
│
├── main.py              # Streamlit app source
├── requirements.txt     # All dependencies
├── .env                 # Environment variables (not committed)
├── README.md            # Project documentation
└── ...
```
---

## 📦 Installation (Local Setup)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/Python-Projects.git
   cd Python-Projects/ResumeRev

2. **Create & Activate a Virtual Environment**

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Add Your Google API Key**
   Create a `.env` file:

   ```
   GOOGLE_API_KEY=your_google_genai_api_key_here
   ```

5. **Run the App**

   ```bash
   streamlit run main.py
   ```

---

## 🔐 Environment Variables

This app requires a **Google API Key** for `google.generativeai`.

Create a `.env` file in the root of your project and add:

```
GOOGLE_API_KEY=your_key_here
```

---

## 🛰️ Deployment

This app is deployed using **[Streamlit Cloud](https://streamlit.io/cloud)**.

### Want to Deploy Your Own?

1. Push code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click **"New app"**, link your repo
4. Set the main file path:

   ```
   ResumeRev/main.py
   ```
5. Under "Advanced settings", add `GOOGLE_API_KEY` in **Secrets**
6. Click **"Deploy"**

---

## 🙋‍♂️ Author

Built with ❤️ by **[Vishnu](https://github.com/VishVandhan004)**

