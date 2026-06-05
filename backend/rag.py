from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import faiss
import numpy as np

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def extract_pdf_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text
def chunk_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(
            text[i:i + chunk_size]
        )

    return chunks

def create_embeddings(chunks):

    embeddings = embedding_model.encode(
        chunks
    )

    return embeddings

def build_vector_store(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        np.array(
            embeddings,
            dtype="float32"
        )
    )

    return index

def search_chunks(
    query,
    chunks,
    index,
    top_k=2
):

    query_embedding = (
        embedding_model.encode(
            [query]
        )
    )

    distances, indices = index.search(
        np.array(
            query_embedding,
            dtype="float32"
        ),
        top_k
    )

    results = []

    for idx in indices[0]:
        results.append(
            chunks[idx]
        )

    return results

def build_context(results):

    return "\n\n".join(results)