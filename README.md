# RAG Document Assistant

A Retrieval-Augmented Generation (RAG) application that allows users to upload documents and ask questions based on their content using a language model.

The system combines document retrieval with LLM generation and is fully containerized using Docker.

---

## Features

- Upload PDF documents
- Question answering based on uploaded content (RAG)
- Conversation history stored in SQLite
- Vector search using ChromaDB
- Persistent storage using Docker volumes
- Web interface built with Flask
- Fully dockerized setup

---

## Tech Stack

- Python 3.11
- Flask
- LangChain
- ChromaDB
- OpenAI API (or configurable LLM)
- SQLite
- Docker + Docker Compose

---
## How it works

1. User uploads a PDF document
2. Document is split into smaller chunks
3. Chunks are converted into embeddings
4. Embeddings are stored in ChromaDB
5. User asks a question
6. Relevant chunks are retrieved
7. LLM generates an answer based on retrieved context

---

## Setup & Run (Docker)

### 1. Clone the repository

Clone the project from GitHub and move into the project directory:

```bash
git clone https://github.com/joannakowalska2507/RAG_Document_Assistant.git
cd RAG_Document_Assistant
```
### 2. Create environment file
```bash 
cp .env.example .env
```
### 3. Then open the file and add your API key:
OPENAI_API_KEY=your_api_key_here

### 4.Build and start the application
```bash
docker compose up --build
```
### 5.Open the application
- After successful startup, open your browser:
http://127.0.0.1:5000