<<<<<<< HEAD
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
=======
# 📄 AI Document Q&A Assistant

This project is a **private AI-powered document assistant** that allows teams to upload internal documents and ask questions about them in natural language — without manually searching through files.

It is designed for **confidential, internal use cases** (legal, HR, policies, technical documentation) and runs entirely on **the client’s infrastructure**.

---

## ✅ What This Tool Does

- Upload documents (`PDF`, `DOCX`, `TXT`)
- Ask questions in plain English
- Receive **accurate answers grounded strictly in the document**
- See which sections of the document were used
- No keyword search, no manual reading

Typical use cases:
- Legal documents & contracts  
- Company handbooks & policies  
- Internal technical documentation  
- Client-specific document sets  

---

## 🔐 Data Privacy & Security

- Documents are processed **only on the client’s server**
- Files are converted into embeddings for semantic search
- Raw documents are **not shared** with third parties
- API keys are provided and managed **by the client**
- No sensitive data is logged or stored externally

This system is suitable for **confidential and sensitive information**.

---

## 🧠 How It Works (High-Level)

1. A document is uploaded through the interface  
2. The document is split into chunks and embedded  
3. Embeddings are stored in a vector database  
4. When a question is asked:
   - Relevant document sections are retrieved
   - An AI model generates an answer **using only that context**

This ensures **grounded, document-based answers**, not hallucinations.

---

## 🖥 User Interface

The application runs as a **web interface**:

- Upload document
- Click “Process”
- Ask questions
- View answers instantly

No technical knowledge is required to use the system.

---

## ⚙️ Deployment & Setup

The project is delivered as a **Dockerized application**.

### Client responsibilities:
- Provide API keys (OpenAI, Pinecone)
- Run the container on their server
- Control access to the application

### What is provided:
- Fully working application
- Docker setup
- Configuration instructions
- Example environment configuration

The system runs as a **single product** — no separate backend setup required.

---

## 🔑 Required Configuration

The following environment variables must be set by the client:

```bash
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
>>>>>>> 35a2bf2 (Initial commit: RAG chatbot (Streamlit + Pinecone))
