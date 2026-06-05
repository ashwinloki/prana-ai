from backend.rag import (
    extract_pdf_text,
    chunk_text,
    create_embeddings,
    build_vector_store,
    search_chunks
)

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

results = search_chunks(
    "What are symptoms of dehydration?",
    chunks,
    index
)

print("\nRESULTS:\n")

for result in results:
    print(result)
    print("-" * 50)