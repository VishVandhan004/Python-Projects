
# 💼 AstraDoc AI — Enterprise Document Intelligence Platform
AstraDoc AI is a professional-grade document intelligence system that enables users to analyze, summarize, and extract factual insights from business documents using NVIDIA's enterprise-scale LLMs. It features two modes: a general-purpose AI assistant and a specialized document analysis suite. The App is deployed on Streamlit Cloud.
---

## 🤖 App is Deployed on Streamlit Cloud
The App is deployed on Streamlit Cloud. Do use it. [Live Demo](https://vishnus-astradoc-ai.streamlit.app/)

---

## 🚀 Features

- 📁 **Multi-Format Support**: Upload and process PDF, DOCX, TXT, and PPTX files, or analyze documents via URLs.
- 🧠 **Executive Summarization**: Generate Brief, Detailed, or Key Point summaries using LLMs.
- ❓ **Document Q&A System**: Ask precise questions about document content and receive grounded, factual answers.
- 💬 **General AI Assistant**: Engage with an intelligent assistant for research, strategy, and technical help.
- 🔒 **Secure API Integration**: Uses environment variables for secure access to NVIDIA's LLM API.
- 🎯 **Token-Aware Processing**: Splits content into intelligent chunks to work with long documents.

---

## 🧰 Tech Stack

| Layer        | Technology                           | Purpose                                   |
|--------------|---------------------------------------|-------------------------------------------|
| **Frontend** | [Streamlit](https://streamlit.io/)   | Fast, interactive web UI                  |
| **Backend**  | Python                                | Core logic and document handling          |
| **LLM**      | NVIDIA (via OpenAI-compatible API)    | Text summarization, Q&A, and conversation |
| **Env Mgmt** | `python-dotenv`                       | Securely store API keys                   |
| **File I/O** | `PyPDF2`, `python-docx`, `python-pptx`| Text extraction from files                |

---

## 📂 File Structure

```bash
AstraDoc/
├── app.py               # Main Streamlit application
├── extract.py           # Custom module to extract text from various file types
├── .env                 # Environment variables (NVIDIA API key)
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 🔑 Prerequisites

- Python 3.8+
- NVIDIA API Key with access to `llama-3.3-nemotron-super-49b-v1`
- Internet access for API requests

---

## 🔧 Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/astradoc-ai.git
cd astradoc-ai

# 2. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your .env file
echo "NVIDIA_API_KEY=your_api_key_here" > .env
```

---

## 🚦 Usage

```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`

---

## 🧠 Modes of Operation

### 💬 AI Chat Assistant

- Interact with the assistant for general-purpose research, brainstorming, or strategy.
- Maintains up to 6 previous messages for conversational memory.

### 📄 Document Intelligence

1. Upload a file or paste a URL.
2. Choose analysis options:
   - Summarize (Brief, Detailed, or Key Points)
   - Ask factual questions from document
3. Receive AI-generated insights directly in the browser.

---

## 📝 Supported File Types

- `.pdf`
- `.docx`
- `.txt`
- `.pptx`

> Unsupported file types are automatically rejected with a user-friendly error.

---

## 🤖 Powered By

### 🔗 NVIDIA LLM via OpenAI-compatible API

- **Model Name:** `nvidia/llama-3.3-nemotron-super-49b-v1`
- **Base URL:** `https://integrate.api.nvidia.com/v1`
- **Integration Method:** `openai.OpenAI()` with custom base URL
- Used for:
  - Summarization
  - Contextual Q&A
  - Conversational interaction

---

## 🧪 Prompt Engineering

### Summarization Prompt
```
Provide a [Brief/Detailed/Key Point] professional summary of this document. Use complete sentences, no bullet points.
```

### Q&A Prompt
```
Answer this question based ONLY on the provided text. Be precise and professional.
```

### Chat Prompt
```
You are a professional AI assistant. Provide concise, helpful responses.
```

---

## 📦 Requirements

```txt
openai
streamlit
python-dotenv
PyPDF2
python-docx
python-pptx
Pillow
requests
beautifulsoup4
lxml
readability-lxml
langchain-community
lxml_html_clean
pypdf
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🛡️ Security Notes

- Your API key is stored locally in a `.env` file and never exposed to the frontend.
- Make sure not to commit `.env` to version control.

---

## 📈 Future Enhancements

- 🔍 Add OCR support for scanned PDFs
- 🧠 Integrate FAISS for vector-based Q&A
- 🔐 Add user authentication (Streamlit login or OAuth)
- 🌐 Deploy via Docker or FastAPI backend
- 📝 Save summary and Q&A results to database
- 📊 Visual analytics on document insights

---

## 🧾 License

This project is intended for educational and enterprise prototype use. For production deployment or commercial use, ensure proper licensing for:
- NVIDIA API usage
- OpenAI-compatible client
- File parsing libraries

---

## 🙋‍♀️ Contributors

Built by Vishnu Vandhan

---

## 🔗 Related Projects

- [Streamlit Docs](https://docs.streamlit.io/)
- [NVIDIA AI Foundation Models](https://developer.nvidia.com/nim)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
