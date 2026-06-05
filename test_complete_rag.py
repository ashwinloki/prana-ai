from backend.rag import (
    extract_pdf_text,
    chunk_text,
    create_embeddings,
    build_vector_store,
    search_chunks,
    build_context
)

from dotenv import load_dotenv
import requests
import os

load_dotenv("backend/.env")

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

# Load PDF
text = extract_pdf_text(
    "medical_docs/sample.pdf"
)

# Create chunks
chunks = chunk_text(text)

# Create embeddings
embeddings = create_embeddings(
    chunks
)

# Build vector store
index = build_vector_store(
    embeddings
)

# User question
question = (
    "What are symptoms of dehydration?"
)

# Retrieve relevant chunks
results = search_chunks(
    question,
    chunks,
    index
)

# Build context
context = build_context(
    results
)

# Build RAG prompt
prompt = f"""
Answer ONLY from the provided context.

If the answer is not present in the context,
reply:

'I could not find this information in the approved medical documents.'

Context:
{context}

Question:
{question}
"""

# Send to OpenRouter
response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization":
        f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type":
        "application/json"
    },
    json={
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
)

result = response.json()

print("\nQUESTION:\n")
print(question)

print("\nCONTEXT USED:\n")
print(context)

print("\nFINAL ANSWER:\n")
print(
    result["choices"][0]
    ["message"]["content"]
)