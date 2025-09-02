from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def answer_and_sources(retriever, question, model_name="gpt-4o-mini"):
    """
    Create a RetrievalQA chain with OpenAI Chat Model and return answer + sources.
    """

    # LLM configuration
    llm = ChatOpenAI(model=model_name, temperature=0)

    # Custom prompt for better context-aware answers
    prompt_template = """
    You are an AI assistant. Use the provided context to answer the question.
    If the answer is not in the context, say "I could not find the answer in the documents."
    
    Context:
    {context}

    Question: {question}

    Answer:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    # RetrievalQA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    # Get result
    result = qa_chain({"query": question})
    return {
        "answer": result["result"],
        "sources": result["source_documents"]
    }
