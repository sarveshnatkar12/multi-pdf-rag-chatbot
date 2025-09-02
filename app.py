import os
import time
import streamlit as st
from dotenv import load_dotenv
from utils.pdf_loader import pdf_loader
from utils.splitter import split_text
from utils.vector_store import create_vector_store
from utils.rag_chain import answer_and_sources

# Load environment variables
load_dotenv()

# Streamlit Page Config
st.set_page_config(page_title="📄 Multi-PDF RAG Chat", page_icon="🤖", layout="wide")

# Custom Dark Theme & Styling
st.markdown("""
<style>
    body, .stApp {
        background-color: #121212;
        color: white;
    }
    .uploaded-pdfs {
        background: #1f1f1f;
        padding: 10px;
        border-radius: 12px;
        margin-bottom: 8px;
        color: #fff;
        font-size: 14px;
    }
    .chat-question {
        background: #2a2a2a;
        color: #fff;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 8px;
        text-align: left;
    }
    .chat-answer {
        background: #333333;
        color: #fff;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: left;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
        background: #1f1f1f;
        color: #fff;
    }
    .emoji {
        font-size: 18px;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Settings
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🤖</h2>", unsafe_allow_html=True)
    st.title("⚙ Settings")
    model_choice = st.selectbox("Choose Model", ["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"])
    if st.button("🗑 Clear Chat"):
        st.session_state.history = []
        st.toast("Chat cleared!", icon="🗑")

st.title("🤖 Multi-PDF RAG Chatbot (OpenAI)")

# API Key Check
if not os.getenv("OPENAI_API_KEY"):
    st.error("❌ OPENAI_API_KEY not found in .env file")
    st.stop()

# Initialize Chat History
if "history" not in st.session_state:
    st.session_state.history = []

# File Uploader
uploaded_files = st.file_uploader(
    "📂 Upload one or more PDF files:",
    type=["pdf"],
    accept_multiple_files=True
)

retriever = None

if uploaded_files:
    st.toast(f"📂 Processing {len(uploaded_files)} file(s)…", icon="📄")

    all_texts, metadatas = [], []
    for uf in uploaded_files:
        with st.spinner(f"Extracting text from {uf.name}..."):
            uf.seek(0)
            raw_text = pdf_loader(uf)

        if not raw_text.strip():
            st.warning(f"No text found in {uf.name}. Skipping.")
            continue

        chunks = split_text(raw_text, chunk_size=1000, chunk_overlap=200)
        all_texts.extend(chunks)
        metadatas.extend([{"source": uf.name}] * len(chunks))

    if not all_texts:
        st.error("No extractable text found in uploaded PDFs.")
        st.stop()

    with st.spinner("🔍 Creating vector store with OpenAI embeddings..."):
        retriever = create_vector_store(texts=all_texts, metadatas=metadatas)

    st.toast("✅ Vector store ready! Ask your question below.", icon="✅")

# Chat UI
if retriever:
    st.markdown("### 💬 Chat with your PDFs")
    question = st.text_input("Type your question and press Enter...")

    if question:
        placeholder = st.empty()  # For typing effect
        with st.spinner("🤔 Thinking..."):
            try:
                result = answer_and_sources(retriever, question, model_name=model_choice)

                # Typing animation
                answer_text = result["answer"]
                typed_answer = ""
                for char in answer_text:
                    typed_answer += char
                    placeholder.markdown(f"<div class='chat-answer'><span class='emoji'>🤖</span>{typed_answer}</div>", unsafe_allow_html=True)
                    time.sleep(0.02)

                st.session_state.history.append({
                    "question": question,
                    "answer": result["answer"],
                    "sources": result["sources"]
                })

            except Exception as e:
                st.error(f"⚠ Error: {e}")

# Display Chat History
if st.session_state.history:
    st.markdown("### 🗨 Chat History")
    for chat in reversed(st.session_state.history):  # latest first
        st.markdown(f"<div class='chat-question'><span class='emoji'>🧑</span><strong>You:</strong> {chat['question']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-answer'><span class='emoji'>🤖</span><strong>AI:</strong> {chat['answer']}</div>", unsafe_allow_html=True)
        with st.expander("📚 View Sources"):
            for i, doc in enumerate(chat["sources"], start=1):
                src = doc.metadata.get("source", "unknown")
                preview = (doc.page_content[:500] + "…") if len(doc.page_content) > 500 else doc.page_content
                st.write(f"**Source {i}: {src}**")
                st.write(preview)
