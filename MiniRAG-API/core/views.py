"""Simple RAG retrieval API built by Sreya Sirivella — ingest, query, reset."""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import ingest_document, search_documents, reset_vector_store
from rest_framework.response import Response
from rest_framework.views import APIView


# This root view where we can see both API endpoints 
# This is only a View and not an API endpoint
class RootView(APIView):
    def get(self, request):
        return Response({
            "ingest": request.build_absolute_uri("/api/ingest/"),
            "query": request.build_absolute_uri("/api/query/?text=example"),
            "reset": request.build_absolute_uri("/api/reset/"),
        })

# Handle POST to /ingest
# Ingest new text to be stored in the vector store.
# Eg- http://127.0.0.1:8000/api/ingest/  <body must have text >
class IngestView(APIView):
    def post(self, request):
        if request.content_type != "application/json":
            return Response({"error": "Content-Type must be application/json"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        text = request.data.get("text")
        text = request.data.get("text", "").strip()
        
        if not isinstance(text, str) or len(text.strip()) < 5:
            return Response({"error": "Text must be a non-empty string of reasonable length."}, status=status.HTTP_400_BAD_REQUEST)

        doc_id = ingest_document(text)
        return Response({"message": "Document ingested.", "id": doc_id}, status=status.HTTP_201_CREATED)

# Handle GET to /query
# Retrieve the most relevant ingested text
# Eg - http://127.0.0.1:8000/api/query/?text=< query here >
class QueryView(APIView):
    def get(self, request):
        query = request.query_params.get("text")
        if not query:
            return Response({"error": "Missing 'text' query param."}, status=status.HTTP_400_BAD_REQUEST)
        
        results = search_documents(query)
        return Response({"results": results})


# Handle POST to /reset
# delete all stored embeddings and documents
# Eg - http://127.0.0.1:8000/api/reset/
class ResetView(APIView):
    def post(self, request):
        success = reset_vector_store()
        if success:
            return Response({"message": "Reset successful"}, status=200)
        else:
            return Response({"error": "Reset failed"}, status=500)
