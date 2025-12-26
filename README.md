# RAG-Chatbot API

A Retrieval-Augmented Generation (RAG) chatbot API that allows users to upload documents (PDF, DOCX, TXT) and ask questions answered **strictly using the document content**.

This project demonstrates an end-to-end LLM system using modern AI engineering tools: document ingestion, vector search, and LLM-based generation.

---

## 🚀 Features

- Upload documents (PDF / DOCX / TXT)
- Chunk and embed documents
- Store embeddings in Pinecone
- Semantic retrieval using vector similarity
- Grounded question answering using an LLM
- Flask-based API
- Designed to be Docker-ready and extensible

---

## 🧠 Architecture Overview

1. **Upload**
   - User uploads a document via API
   - File is saved locally

2. **Ingestion**
   - Document is loaded and split into chunks
   - Chunks are embedded
   - Embeddings + metadata are stored in Pinecone

3. **Query**
   - User submits a question
   - Question is embedded
   - Relevant chunks are retrieved from Pinecone
   - Retrieved context is injected into an LLM prompt
   - Answer is generated using only document context

---

## 🛠️ Tech Stack

- Python
- Flask
- LangChain (LCEL)
- OpenAI (embeddings + chat models)
- Pinecone (vector database)
- Docker (optional deployment)

---

## 📡 API Endpoints

### `POST /upload`
Uploads a document.

- Content-Type: `multipart/form-data`
- Field name: `file`

Returns metadata about the uploaded file.

---

### `POST /ask`
Ask a question about the uploaded document.

```json
{
  "question": "What is the refund policy?"
}# RAG-Chatbot
