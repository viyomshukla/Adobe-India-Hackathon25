# Persona-Driven Document Intelligence

This project is a full-stack application for persona-driven document intelligence. It enables users to upload a set of PDFs and a persona/job description, and receive a tailored analysis of the documents based on the persona’s needs. The backend is built with Python (FastAPI), and the frontend is a ReactJS app.

---

## Features

- **Persona-Driven Analysis:** Extracts and ranks the most relevant sections from uploaded PDFs based on a user-defined persona and job-to-be-done.
- **Automatic Section Identification:** Uses NLP to identify and extract meaningful sections from documents.
- **Semantic Relevance Ranking:** Ranks document sections using sentence embeddings and persona/job keywords.
- **Easy-to-Use Web Interface:** Upload PDFs and input.json, trigger analysis, and download results.
- **Dockerized Backend:** Simple deployment and reproducibility.

---

## Project Structure

```
adobe/
  ├── main.py                  # Core document intelligence logic
  ├── main_api.py              # FastAPI backend server
  ├── requirements.txt         # Python dependencies
  ├── Dockerfile               # Backend Docker build instructions
  ├── download_models.py       # Model download script
  ├── download_st_model.py     # SentenceTransformer model download
  ├── frontend/                # ReactJS frontend app
  │   ├── src/
  │   │   ├── App.js           # Main React app
  │   │   └── ...
  │   ├── public/
  │   │   └── index.html
  │   └── package.json         # Frontend dependencies
  └── ...
```

---

## Architecture

- **Backend:** Python (FastAPI)
  - Accepts `input.json` and PDFs via `/analyze/` endpoint
  - Processes documents using NLP and semantic ranking
  - Returns a tailored JSON output
- **Frontend:** ReactJS
  - Uploads files to backend
  - Shows progress/errors
  - Provides download link for results
- **Docker:** Backend is containerized for easy deployment

---

## Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for backend)
- [Node.js & npm](https://nodejs.org/) (for frontend development)

### 1. Backend (Docker)

Build and run the backend API:

```sh
# In the adobe/ directory
# Build the Docker image
docker build -t persona-doc-intel-backend .

# Run the backend container
# (Exposes port 8000 by default)
docker run -p 8000:8000 persona-doc-intel-backend
```

### 2. Frontend (ReactJS)

```sh
cd frontend
npm install
npm start
```
- The frontend will run on [http://localhost:3000](http://localhost:3000) by default.
- Make sure the backend is running on port 8000 for API requests to work.

---

## Usage

1. **Prepare your files:**
   - `input.json` (specifies persona, job, and document filenames)
   - PDFs (must match filenames in `input.json`)
2. **Open the frontend:**
   - Go to [http://localhost:3000](http://localhost:3000)
3. **Upload files:**
   - Upload `input.json` and all required PDFs
   - Click **Analyze**
4. **Download results:**
   - When processing is complete, download `challenge1b_output.json`

---

## Example `input.json`

```json
{
  "persona": { "role": "Researcher" },
  "job_to_be_done": { "task": "Find key findings and methodology" },
  "documents": [
    { "filename": "Document1.pdf" },
    { "filename": "Document2.pdf" }
  ]
}
```

---
Screeshots:<img width="1600" height="900" alt="Image" src="https://github.com/user-attachments/assets/fbb136c6-e4de-4756-80a3-a76456fbf321" />

## Troubleshooting

- **Docker error:**
  - Ensure Docker Desktop is running before building or running the backend container.
- **Frontend cannot connect to backend:**
  - Make sure backend is running on port 8000 and accessible.
- **File upload errors:**
  - Ensure all PDFs listed in `input.json` are uploaded.

---

## Made By
Viyom shukla,Nikhil sharma,utkarsh mishra
