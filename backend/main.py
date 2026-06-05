from backend.rag import (
    extract_pdf_text,
    chunk_text,
    create_embeddings,
    build_vector_store,
    search_chunks,
    build_context
)
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List
import requests
import os

# Load environment variables
load_dotenv()

# Get OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Load and prepare RAG knowledge base

text = extract_pdf_text(
    "medical_docs/sample.pdf"
)

chunks = chunk_text(text)

embeddings = create_embeddings(
    chunks
)

index = build_vector_store(
    embeddings
)

# Create FastAPI app
app = FastAPI()


# Request schema
class ChatRequest(BaseModel):
    message: str
    history: List[dict]


# Home route
@app.get("/")
def home():
    return {
        "message": "Prana AI Backend Running with OpenRouter"
    }

def detect_intent(question):

    question = question.lower().strip()

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    introductions = [
        "my name is",
        "i am",
        "i'm"
    ]

    if question in greetings:
        return "greeting"

    for intro in introductions:
        if question.startswith(intro):
            return "introduction"

    return "medical_query"


@app.post("/chat")
def chat(request: ChatRequest):

    question = request.message

    intent = detect_intent(question)

    if intent == "greeting":

        return {
            "response":
            "Hello! I'm Prana AI. How can I assist you with your healthcare questions today?"
        }

    if intent == "introduction":

        return {
            "response":
            "Nice to meet you! I'm Prana AI. Feel free to ask me any healthcare-related questions."
        }


    # Retrieve relevant chunks
    results = search_chunks(
        question,
        chunks,
        index
    )

    context = build_context(
        results
    )

    prompt = f"""
Answer ONLY using the provided context.

If the answer is not found in the context,
reply exactly:

I could not find this information in the approved medical documents.

Context:
{context}

Question:
{question}
"""

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
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

    print(result)

    if "choices" not in result:
        return {
            "error": result
        }

    return {
        "response":
        result["choices"][0]["message"]["content"]
    }