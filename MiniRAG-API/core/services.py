
import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = 'all-MiniLM-L6-v2'
DOC_PATH = os.path.join(os.path.dirname(__file__), 'doc_store', 'doc_map.pkl')
INDEX_PATH = os.path.join(os.path.dirname(__file__), 'doc_store', 'faiss_index.idx')

model = SentenceTransformer(MODEL_NAME)

# Load FAISS index or create a new one if not present 
def load_index():
    if not os.path.exists(INDEX_PATH):
        return faiss.IndexFlatIP(384)
    return faiss.read_index(INDEX_PATH)

def load_documents():
    if not os.path.exists(DOC_PATH):
        return []
    with open(DOC_PATH, 'rb') as f:
        return pickle.load(f)

def save_documents(docs):
    with open(DOC_PATH, 'wb') as f:
        pickle.dump(docs, f)

def save_index(index):
    faiss.write_index(index, INDEX_PATH)

# Normalize vectors for cosine similarity
def normalize(vectors):
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)


# Embed and store a new document
def ingest_document(text):

    docs = load_documents()
    doc_id = len(docs) + 1
    docs.append({'id': doc_id, 'text': text})
    save_documents(docs)

    embedding = model.encode([text], convert_to_numpy=True)
    embedding = normalize(embedding)

    index = load_index()
    index.add(embedding)
    save_index(index)

    return doc_id

# Search for top-k documents similar to the query
# k =3 in this case 
def search_documents(query, top_k=3):
    docs = load_documents()
    if not docs:
        return []

    query_embedding = model.encode([query], convert_to_numpy=True)
    query_embedding = normalize(query_embedding)

    index = load_index()
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i, dist in zip(indices[0], distances[0]):
        if i < len(docs):
            results.append({
                'id': docs[i]['id'],
                'text': docs[i]['text'],
                'similarity': float(dist)
            })
    return results

# Deletes FAISS index and doc map
def reset_vector_store():
    if os.path.exists(DOC_PATH):
        os.remove(DOC_PATH)
    if os.path.exists(INDEX_PATH):
        os.remove(INDEX_PATH)
    return True