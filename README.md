# 📄 Private Document Q&A (RAG Assistant)

This is a **private AI-powered Document Q&A tool** for teams who need to ask questions about internal documents (policies, handbooks, contracts, technical docs) without manually searching.

✅ Upload a document → Process → Ask questions  
✅ Answers are generated **only from your document context** (grounded / RAG)

---

## What the Client Gets

- A simple web app UI to:
  - Upload a document (`PDF`, `DOCX`, `TXT`)
  - Process it for search
  - Ask questions in plain English
- Document-based answers (not generic chatbot answers)
- “Private-by-default” deployment: runs on **your infrastructure**

---

## Typical Use Cases

- Legal: contracts, lawsuits, internal memos  
- HR: employee handbook, policies, onboarding docs  
- Engineering: internal documentation, runbooks, SOPs  
- Any “read this long file for me” workflow

---

## Data & Privacy Notes (Important)

- The application is intended to run on the client’s server / environment.
- Your document is chunked and embedded to enable semantic search.
- API keys are **provided and managed by the client**.
- Do not upload documents you are not allowed to process.

*(If you require stricter privacy guarantees, this can be adapted to run with self-hosted models / private networking.)*

---

## Requirements (Client)

You will need:
- Docker installed (recommended)
- API keys:
  - `OPENAI_API_KEY` (LLM + embeddings)
  - `PINECONE_API_KEY` (vector database)

Optional (depending on Pinecone setup):
- Pinecone index name / environment / region settings (if your build uses them)

---

## Run the App (Docker)

### 1) Pull the image
```bash
docker pull anzepislar/<IMAGE_NAME>:<TAG>