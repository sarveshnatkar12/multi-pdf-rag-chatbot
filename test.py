import os
from dotenv import load_dotenv
from utils.pdf_loader import pdf_loader
from utils.splitter import split_text
from utils.vector_store import create_vector_store
from utils.rag_chain import answer_and_sources

# Load environment variables
load_dotenv()

# 1. Check API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY missing in .env file")

print("✅ OpenAI API Key loaded successfully.\n")

# 2. Provide a local test PDF path
test_pdf_path = "chapter9.pdf"  # Update with your file name
if not os.path.exists(test_pdf_path):
    raise FileNotFoundError(f"Test PDF not found at {test_pdf_path}")

# 3. Extract text
print("📄 Extracting text from PDF...")
with open(test_pdf_path, "rb") as f:
    text = pdf_loader(f)

if not text.strip():
    raise ValueError("No text extracted from PDF.")
print(f"✅ Extracted {len(text)} characters of text.\n")

# 4. Split text
chunks = split_text(text)
print(f"✅ Split into {len(chunks)} chunks.\n")

# 5. Create vector store
print("📦 Creating vector store...")
retriever = create_vector_store(chunks)
print("✅ Vector store ready.\n")

# 6. Multiple Questions Testing
questions = [
    "What is the main topic of Chapter 9?",
    "Explain the concept of simple linear regression described in this chapter.",
    "What assumptions does linear regression make according to this chapter?",
    "What is the formula for linear regression mentioned in the document?",
    "What are residuals in the context of linear regression?"
]

print("🔍 **Starting Question-Answer Testing** 🔍\n")

for idx, question in enumerate(questions, start=1):
    print(f"❓ Question {idx}: {question}")
    result = answer_and_sources(retriever, question)
    
    print("✅ Answer:")
    print(result["answer"])
    
    print("\n📚 Top Source Preview:")
    for doc in result["sources"][:1]:
        preview = (doc.page_content[:300] + "...") if len(doc.page_content) > 300 else doc.page_content
        print(preview)
    
    print("\n" + "-" * 80 + "\n")
