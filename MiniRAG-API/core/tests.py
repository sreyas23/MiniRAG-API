from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import subprocess

class RAGAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ingest_url = "/api/ingest/"
        self.query_url = "/api/query/"
        self.reset_url = "/api/reset/"

    # test case to  check ingestion of valid text 
    # API should return a 201 status code and include an "id" in the response
    def test_ingest_valid_text(self):
        response = self.client.post(self.ingest_url, {"text": "This is a test doc."}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

    # test case to check ingestion of empty text
    # API should return a 400 status code and include an "error" message in the response
    def test_ingest_missing_text_field(self):
        response = self.client.post(self.ingest_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    # test case to check ingestion of text that is too short
    # API should return a 400 status code and include an "error" message in the response
    def test_ingest_short_text(self):
        response = self.client.post(self.ingest_url, {"text": "Hi"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    # test case to check ingestion of text data in a different content type instead of application/json
    # API should return a 415 status code and include an "error" message in the response
    def test_ingest_invalid_content_type(self):
        response = self.client.post(
            self.ingest_url,
            data='{"text": "This is raw JSON, but wrong content type"}',
            content_type="text/plain"
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertIn("error", response.data)

    # test case to check querying of valid text
    # API should return a 200 status code, include "results" in the response and the results should not be empty
    def test_query_valid_text(self):
        self.client.post(self.ingest_url, {"text": "Civic is great for communication automation."}, format="json")
        response = self.client.get(self.query_url, {"text": "automation"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertGreater(len(response.data["results"]), 0)

    # test case to check querying of text that is not present
    # API should return a 404 status code and include an "error" message in the response
    def test_query_missing_text_param(self):
        response = self.client.get(self.query_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    # test case to check the reset functionality
    # API should return a 200 status code and include a "message" in the response
    def test_reset_endpoint(self):
        response = self.client.post(self.reset_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Reset successful")
    

    # re ingest the original data after all the tests are performed   
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("\nRe-ingesting original documents after reset...")

        documents = [
            {"id": 1, "text": "Civic is an AI mail assistant that modernizes constituent communications through email, phone, and mail automation, providing advanced analytics to measure engagement."},
            {"id": 2, "text": "Retrieval-Augmented Generation (RAG) is a technique that integrates external knowledge sources into generative models for more accurate and context-aware responses."},
            {"id": 3, "text": "At Civic, we believe in streamlining an organization’s communication workflow, reducing the manual labor of sorting and responding to large volumes of messages."},
            {"id": 4, "text": "Unlike traditional identity verification platforms, Civic's focus is on bridging the gap between users and organizations through intelligent communications pipelines."},
            {"id": 5, "text": "The Redwood Forest in California is home to some of the tallest trees on Earth, known as coast redwoods, which can reach several hundred feet in height."},
            {"id": 6, "text": "San Francisco is a cultural and financial center in California, well-known for iconic landmarks like the Golden Gate Bridge, as well as its thriving tech scene."},
            {"id": 7, "text": "Naive Bayes is a simple yet powerful probabilistic classifier based on Bayes' theorem with strong independence assumptions, frequently used in text classification tasks."}
        ]

        client = APIClient()
        for doc in documents:
            response = client.post("/api/ingest/", {"text": doc["text"]}, format="json")
        
        print("Re-ingesting successful")