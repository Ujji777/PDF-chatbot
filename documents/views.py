from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UploadedDocument
from .serializers import UploadedDocumentSerializer
from .utils import extract_text_from_pdf, extract_text_from_image_pdf
from .embedding_service import chunk_text, embed_and_store
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class UploadDocumentAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = UploadedDocumentSerializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save()
            file_path = document.file.path

            try:
                # Try text-based extraction first
                text = extract_text_from_pdf(file_path)
                if not text.strip():
                    # Fallback to OCR
                    text = extract_text_from_image_pdf(file_path)

                # Save extracted text to model
                document.extracted_text = text
                document.save()

                # Chunk and embed
                chunks = chunk_text(text)
                embedded_count = embed_and_store(document.id, chunks)

                return Response({
                    "message": "File uploaded, text extracted, and embedded.",
                    "document_id": document.id,
                    "embedded_chunks": embedded_count,
                    "extracted_text": text[:1000] + "..." if len(text) > 1000 else text
                })

            except Exception as e:
                return Response({"error": str(e)}, status=500)

        return Response(serializer.errors, status=400)




# class QueryDocumentAPIView(APIView):
#     parser_classes = [JSONParser]

#     def post(self, request, *args, **kwargs):
#         question = request.data.get("question")
#         if not question:
#             return Response({"error": "Missing 'question' in request."}, status=400)

#         try:
#             # Initialize embedding model and Chroma vector store
#             embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#             vectorstore = Chroma(
#                 embedding_function=embeddings,
#                 persist_directory="vector_store"
#             )

#             # Perform semantic search
#             results = vectorstore.similarity_search(question, k=5)

#             # Extract matched chunks and return as response
#             matches = [{"text": doc.page_content, "metadata": doc.metadata} for doc in results]

#             return Response({
#                 "question": question,
#                 "matches": matches
#             })

#         except Exception as e:
#             return Response({"error": str(e)}, status=500)
        

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from .theme_extractor import extract_themes_from_chunks
from .llm_answer import synthesize_answer  
import os

class QueryDocumentAPIView(APIView):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        question = request.data.get("question")
        if not question:
            return Response({"error": "Missing 'question'."}, status=400)

        try:
            # Load vector store
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            vectorstore = Chroma(embedding_function=embeddings, persist_directory="vector_store")

            # Perform search
            results = vectorstore.similarity_search(question, k=5)

            # Generate answer
            final_answer = synthesize_answer(question, results)

            # Extract themes
            themes = extract_themes_from_chunks(results)

            # Format results
            citations = []
            for doc in results:
                meta = doc.metadata
                citations.append({
                    "document_id": f"DOC{meta.get('doc_id', '?').zfill(3)}",
                    "extracted_answer": doc.page_content.strip().split("\n")[0][:150],
                    "citation": f"Page {meta.get('page', '?')}, Para {meta.get('para', '?')}"
                })

            return Response({
                "question": question,
                "answer": final_answer,
                "themes": themes,
                "citations": citations
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)

