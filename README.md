# MiniRAG-API
I built a small retrieval API with Django/DRF that lets me post text, embed it with MiniLM, store vectors in FAISS, and ask for the closest matches. It runs locally on CPU, keeps a simple on-disk index, and exposes clean endpoints for ingest, query, and reset basically the retrieval layer I can drop behind any LLM.
