# ContextCoach API 🚀

> A production-structured, containerized backend microservice built for AI-driven personal development and digital coaching platforms. Implements a Retrieval-Augmented Generation (RAG) pipeline architecture.

## 🛠️ Tech Stack
* **Language & Framework:** Python 3.12, FastAPI, Pydantic (strict data validation)
* **Architecture:** RAG (Retrieval-Augmented Generation) pattern for context injection
* **Testing & Quality:** Pytest automated test suite
* **Cloud & DevOps:** Docker-ready, optimized for deployment on Microsoft Azure (App Service / Container Apps)

---

## 📌 Project Overview
ContextCoach is designed to bridge the gap between backend engineering and generative AI workflows. It simulates a core backend system that ingests personal development notes/documents, indexes them, and processes intelligent, context-aware coaching queries.

---

## 🚀 Getting Started Locally

### 1. Clone the Repository
```bash
git clone https://github.com/hungnguyenrfh/context-coach.git
cd context-coach
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# On Windows (PowerShell):
venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Development Server
```bash
uvicorn app.main:app --reload
```
The API will be live at `http://127.0.0.1:8000`. You can explore and test the interactive endpoints via Swagger UI at `http://127.0.0.1:8000/docs`.

---

## 🧪 Running Automated Tests
To execute the automated test suite and verify software quality:
```bash
pytest -v
```

---

## 🐳 Docker Deployment (Azure Ready)
To build and run the application inside a container:
```bash
docker build -t context-coach .
docker run -p 8000:8000 context-coach
```