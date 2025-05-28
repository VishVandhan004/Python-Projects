# 📦 Standard and Third-party Imports
import os  # For interacting with the operating system (e.g., reading env vars)
import streamlit as st  # Streamlit for building the web-based user interface
from dotenv import load_dotenv  # For loading environment variables from a .env file
from openai import OpenAI  # NVIDIA-compatible OpenAI SDK for API calls
import extract  # Custom Python module containing functions to extract text from various document formats

# 🌍 Load environment variables (like API keys)
load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")  # Fetch NVIDIA API key from the environment

# 🤖 Initialize the OpenAI-compatible client (pointing to NVIDIA’s LLM endpoint)
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",  # NVIDIA-hosted OpenAI-compatible API
    api_key=api_key
)

# 🔢 Configuration Constants
MAX_TOKENS = 3000  # Token limit per chunk when processing documents
OVERLAP = 500  # Overlap between chunks for better summarization continuity
MODEL_NAME = "nvidia/llama-3.3-nemotron-super-49b-v1"  # Selected NVIDIA LLM model
APP_NAME = "AstraDoc AI"  # Display name of the application
APP_ICON = "💼"  # Emoji/icon shown in the browser tab

# 💾 Streamlit Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Store chat messages for persistence

if "doc_session" not in st.session_state:
    st.session_state.doc_session = {
        "processed_text": "",  # Extracted text from the document
        "summary": "",  # Cached summary text
        "qa_ready": False  # Flag indicating whether Q&A can begin
    }

# --------------------------
# 📚 Document Processing Logic
# --------------------------

# 🔗 Split large documents into chunks for summarization
def chunk_text(text, max_tokens=MAX_TOKENS, overlap=OVERLAP):
    chunk_size = max_tokens * 4  # Roughly estimate bytes per token
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size - overlap)]

# ✏️ Summarize a single chunk of text using the NVIDIA LLM
def summarize_chunk(content, summary_type, max_output_tokens):
    prompt = f"Provide a {summary_type} professional summary of this document. Use complete sentences, no bullet points:\n\n{content}"
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are an executive summary assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        top_p=0.95,
        max_tokens=max_output_tokens,
        stream=False
    )
    return response.choices[0].message.content.strip()

# 📄 Summarize a full document by processing it in chunks
def summarize_file(full_text, summary_type):
    token_map = {"Brief": 500, "Detailed": 1024, "Key Points": 800}  # Output size mapping
    chunks = chunk_text(full_text)  # Split into chunks
    return "\n\n".join(summarize_chunk(chunk, summary_type, token_map[summary_type]) for chunk in chunks)

# ❓ Find an answer to a user question from the document
def find_answer_in_text(text, question):
    prompt = f"""Answer this question based ONLY on the provided text. Be precise and professional:

Text:
\"\"\"{text}\"\"\"

Question: {question}

Respond with ONLY the factual answer."""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a factual Q&A system."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=512,
        stream=False
    )
    answer = response.choices[0].message.content.strip()
    return answer if answer.lower() != "i don't know" else "Answer not found in document."

# --------------------------
# 💬 AI Chat Interaction
# --------------------------

# Handles chat interface and appends messages to session
def chat_with_ai(user_message):
    st.session_state.chat_history.append({"role": "user", "content": user_message})

    messages = [
        {"role": "system", "content": "You are a professional AI assistant. Provide concise, helpful responses."}
    ] + [
        {"role": msg["role"], "content": msg["content"]}
        for msg in st.session_state.chat_history[-6:]  # Limit history to last 6 messages
    ]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
        stream=False
    )

    ai_response = response.choices[0].message.content.strip()
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    return ai_response

# --------------------------
# 🎨 Streamlit UI Setup
# --------------------------

# Page-level UI settings
st.set_page_config(
    page_title=APP_NAME,
    layout="wide",
    page_icon=APP_ICON,
    menu_items={
        'About': f"### {APP_NAME}\nProfessional Document Intelligence Platform"
    }
)

# Sidebar Navigation
app_mode = st.sidebar.radio(
    "Application Mode",
    ["💬 AI Chat Assistant", "📄 Document Intelligence"],
    index=0  # Default selection
)

# --------------------------
# 💬 Chat Assistant UI
# --------------------------

if "AI Chat Assistant" in app_mode:
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='font-weight: 700;'>AstraDoc AI Assistant</h1>
        <h3 style='color: #666;'>Professional Knowledge Companion</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    ### 💬 General Intelligence Features:
    - Research and analysis
    - Technical explanations
    - Business strategy
    - Creative brainstorming
    """)

    # Render chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input and response generation
    if prompt := st.chat_input("Ask me anything..."):
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                response = chat_with_ai(prompt)
            st.write(response)

# --------------------------
# 📄 Document Intelligence UI
# --------------------------

else:
    if not st.session_state.doc_session.get("processed_text"):
        # Introductory hero section
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1 style='font-weight: 700;'>AstraDoc AI Assistant</h1>
            <h3 style='color: #666;'>Enterprise Document Processing Suite</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        cols = st.columns(2)
        with cols[0]:
            st.markdown("### 🚀 Key Features")
            st.markdown("""
            - **Smart Document Analysis**
            - **Precision Q&A System**
            - **Multi-Format Support**
            - **Military-Grade Security**
            """)
        with cols[1]:
            st.markdown("### 💡 How It Works")
            st.markdown("""
            1. Upload any document
            2. Choose your analysis type
            3. Get AI-powered insights
            """)
        st.markdown("---")

    # Sidebar file input
    st.sidebar.header("Document Input")
    input_mode = st.sidebar.radio("Source", ["Upload File", "Enter URL"], horizontal=True)
    uploaded_file = None
    url_input = ""

    if input_mode == "Upload File":
        uploaded_file = st.sidebar.file_uploader(
            "Select file",
            type=["pdf", "txt", "docx", "pptx"],
            label_visibility="collapsed"
        )
    else:
        url_input = st.sidebar.text_input("Document URL", placeholder="https://...")

    # Trigger document processing
    if st.sidebar.button("Process Document", type="primary"):
        with st.spinner("Analyzing document..."):
            if input_mode == "Upload File" and uploaded_file:
                file_ext = uploaded_file.name.split('.')[-1].lower()
                if file_ext == "pdf":
                    text = extract.extract_text_from_pdf(uploaded_file)
                elif file_ext == "txt":
                    text = extract.extract_text_from_txt(uploaded_file)
                elif file_ext == "docx":
                    text = extract.extract_text_from_docx(uploaded_file)
                elif file_ext == "pptx":
                    text = extract.extract_text_from_pptx(uploaded_file)
                else:
                    st.error("Unsupported file format")
                    st.stop()
            elif url_input:
                text = extract.extract_text_from_url(url_input)
            else:
                st.error("No input provided")
                st.stop()

            # Store extracted text in session
            st.session_state.doc_session["processed_text"] = text
            st.session_state.doc_session["qa_ready"] = True
            st.success("Document processed successfully!")

    # Document summary or Q&A operations
    if st.session_state.doc_session.get("processed_text"):
        st.sidebar.header("Analysis Tools")
        operation = st.sidebar.radio("Operation", ["📝 Summarize", "❓ Document Q&A"], index=0)

        # 📝 Summarization UI
        if "Summarize" in operation:
            st.markdown("## Executive Summary")
            summary_type = st.selectbox("Summary Style", ["Brief", "Detailed", "Key Points"], index=0)

            if st.button("Generate Summary"):
                with st.spinner("Creating professional summary..."):
                    summary = summarize_file(
                        st.session_state.doc_session["processed_text"],
                        summary_type
                    )
                    st.session_state.doc_session["summary"] = summary
                st.text_area("Summary", value=summary, height=300, label_visibility="collapsed")

        # ❓ Q&A UI
        elif "Q&A" in operation:
            st.markdown("## Document Interrogation")
            question = st.text_input("Ask about the document content:")

            if question and st.session_state.doc_session["qa_ready"]:
                with st.spinner("Extracting precise answer..."):
                    answer = find_answer_in_text(
                        st.session_state.doc_session["processed_text"],
                        question
                    )
                st.success("Verified Answer:")
                st.info(answer)

# --------------------------
# 🔚 Footer Section
# --------------------------
st.sidebar.markdown("---")
st.sidebar.markdown(f"**{APP_NAME} v2.1**")
st.sidebar.markdown("*Enterprise Document AI*")
