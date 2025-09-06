# Multi-PDF RAG Chatbot using OpenAI and LangChain

A Retrieval-Augmented Generation (RAG) chatbot built with **OpenAI GPT models**, **LangChain**, and **Streamlit**.  
This application allows users to upload multiple PDF documents, ask natural language questions, and get accurate answers with sources.

---

## Features
- Upload multiple PDF documents  
- Extract, split, and store text in a vector database (ChromaDB)  
- Ask questions and get context-aware answers  
- Dark Mode UI for professional look  
- Chat history with previous questions and answers  
- Real-time typing effect for answers  
- Powered by OpenAI GPT models (gpt-4o-mini / gpt-4 / gpt-3.5)

---

## Screenshots

### Home Page
![Home](assets/home.png)

### PDF Upload
![Upload](assets/upload.png)

### Chat Interface
![Chat](assets/chat.png)



---

## Tech Stack
- **Python 3.10+**
- [Streamlit](https://streamlit.io/) - UI Framework
- [LangChain](https://www.langchain.com/) - RAG Pipeline
- [OpenAI API](https://platform.openai.com/) - GPT Models & Embeddings
- [ChromaDB](https://www.trychroma.com/) - Vector Database
- [PyPDF](https://pypi.org/project/pypdf/) - PDF Text Extraction

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/multi-pdf-rag-chatbot.git
cd multi-pdf-rag-chatbot
```
##2. Create Virtual Environment & Install Dependencies
```
python -m venv RAGBot
source RAGBot/bin/activate   # (On Mac/Linux)
RAGBot\Scripts\activate      # (On Windows)

pip install -r requirements.txt
```
3. Add OpenAI API Key

Create a .env file in the root directory:
```
OPENAI_API_KEY=your_api_key_here
```
4. Run the App
```
streamlit run app.py
```
Example Questions for Chapter 9 PDF:

What is the main topic of Chapter 9?

Explain the concept of simple linear regression described in this chapter.

What assumptions does linear regression make?

What is the formula for linear regression?

What are residuals in linear regression?

Project Structure
```
multi-pdf-rag-chatbot/
│── app.py                  # Streamlit App
│── test.py                 # Local Testing Script
│── .env                    # API Key
│── requirements.txt        # Dependencies
│── utils/
│   ├── pdf_loader.py       # PDF Text Extraction
│   ├── splitter.py         # Text Chunking
│   ├── embeddings.py       # OpenAI Embeddings
│   ├── vector_store.py     # ChromaDB Vector Store
│   ├── rag_chain.py        # QA Chain with OpenAI
│── assets/
│   ├── home.png            # Screenshot 1
│   ├── upload.png          # Screenshot 2
│   ├── chat.png            # Screenshot 3
│   ├── demo-thumbnail.png  # Video Thumbnail

