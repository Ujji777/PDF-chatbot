A document-aware chatbot built using Django REST Framework, Groq (LLaMA 3), LangChain, and OCR. It allows you to upload PDFs (including scanned image PDFs), extract text via OCR if needed, store embeddings, and query the documents using a powerful LLM — all inside a Dockerized app.
 Features
Upload text-based or image-based PDFs

Extract text using PyMuPDF and fallback to OCR (pytesseract)

Chunk and embed content using LangChain + HuggingFaceEmbeddings

Store in Chroma vector DB

Query documents using Groq’s LLaMA 3 for answers

Fully containerized with Docker

Tech Stack
Python + Django REST Framework

LangChain + HuggingFaceEmbeddings

Groq API (LLaMA 3)

Chroma (in-memory vector DB)

pytesseract + pdf2image (OCR)

Docker

Setup Instructions
1️. Clone the repo
bash
Copy
Edit
git clone https://github.com/Ujji777/UJJWAL-Tak-wasserstoff-AiInternTask.git
cd UJJWAL-Tak-wasserstoff-AiInternTask
2️. Create a .env file
Create a file named .env in the root of the project:

env
Copy
Edit
GROQ_API_KEY=your_groq_api_key_here
DEBUG=True
 You can get a free Groq key from: https://console.groq.com/keys

3️. Run using Docker
bash
Copy
Edit
docker build -t chatbot-app .
docker run -p 8000:8000 --env-file .env chatbot-app
Now visit: http://localhost:8000/

 API Endpoints
📤 Upload Document (with OCR fallback)
POST /api/upload/

form-data body:

Key	Type	Value
file	File	Your PDF document

Response:

json
Copy
Edit
{
  "message": "File uploaded, text extracted, and embedded.",
  "document_id": 1,
  "embedded_chunks": 12,
  "extracted_text": "Penalty provisions..."
}
* Query the Document
POST /api/query/

JSON body:

json
Copy
Edit
{
  "question": "What is the penalty under the SEBI Act?"
}
Response:

json
Copy
Edit
{
  "question": "What is the penalty under the SEBI Act?",
  "answer": "According to the SEBI Act, the penalty can be up to ₹25 crore...",
  "themes": ["SEBI", "Penalty", "Regulatory Act"],
  "citations": [
    {
      "document_id": "1",
      "extracted_answer": "Under section 15A...",
      "citation": "Page 3"
    }
  ]
}
📦 Folder Structure
bash
Copy
Edit
chatbot_project/
├── documents/                  # Django app
│   ├── views.py
│   ├── models.py
│   ├── utils.py                # PDF + OCR extraction
│   ├── embedding_service.py   # Chunk, embed, store
│   └── ...
├── vector_store/              # Chroma DB
├── hf_cache/                  # HuggingFace model cache
├── manage.py
├── Dockerfile
└── requirements.txt
* Run Locally (Optional)
If you prefer not to use Docker:

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
📬 Postman Test Collection
You can test the endpoints using Postman:

Set URL to http://localhost:8000/api/upload/ or /api/query/

Use form-data or raw JSON as shown above

# Credits
Built by Ujjwal Tak as part of a Gen-AI Project.
Inspired by real-world use cases of OCR + vector-based retrieval + LLM response generation.

