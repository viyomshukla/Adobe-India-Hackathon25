# 🧾 Round 1A: Document Outline Extraction Task

## 🧩 Theme: Making Sense of Documents Structurally

---

## 🧠 Objective

This solution programmatically analyzes PDF documents and generates a structured hierarchical outline, including:
- **Document title**
- All headings categorized as **H1, H2, and H3**
- The **text content** and **page number** of each heading

The output is a JSON file per PDF, matching the following format:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

---

## ⚙️ Approach & Models/Libraries Used

### Backend
- **Flask**: Lightweight Python web framework for the API.
- **PyMuPDF (fitz)**: For fast, reliable PDF parsing and text extraction.
- **flask_cors**: To enable CORS for frontend-backend communication.
- **No ML models**: The solution is heuristic-based (font size, font weight, position) and does not use any large pre-trained models.

### Frontend
- **React**: Modern JavaScript library for building user interfaces.
- **No ML models**: The frontend is a simple React app for file upload and result display.

---

## ▶️ How to Build and Run the Solution

### Backend (Flask API) with Docker

1. **Install Docker** (if not already):
   - Download from https://www.docker.com/products/docker-desktop/
   - Start Docker Desktop.

2. **Build the Docker image:**
   ```sh
   docker build -t pdf-outline-backend .
   ```

3. **Run the backend container:**
   ```sh
   docker run -p 5000:5000 pdf-outline-backend
   ```
   - The API will be available at [http://localhost:5000](http://localhost:5000)

### Frontend (React App)

1. Open a new terminal and navigate to the frontend directory:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the frontend:
   ```sh
   npm start
   ```
   - The app will open at [http://localhost:3000](http://localhost:3000)

---

## 🛠️ API Usage

- **Endpoint:** `POST /extract-outline`
- **Description:** Accepts one or more PDF files and returns a JSON outline for each.
- **How to use:**
  - Use the frontend UI, or
  - Use a tool like Postman/curl to POST PDF(s) to `http://localhost:5000/extract-outline` with form-data key `files`.

---

## 📦 Dependencies

- Python 3.8+
- Flask
- PyMuPDF (`fitz`)
- flask_cors
- Node.js (for frontend)
- React, react-scripts (see `frontend/package.json`)

All backend dependencies are listed in `requirements.txt`.

---

## 📂 File Structure

```
app/
  input/      # Input PDFs
  output/     # Output JSONs
  main.py     # Batch script
  api.py      # Flask API
frontend/
  src/        # React source code
  ...         # React config files
requirements.txt
Dockerfile
README.md
```

---

## 🚦 Runtime & Resource Constraints

- No internet access required.
- Model-free (no >200MB models used).
- CPU-only, completes a 50-page PDF in under 10 seconds (on typical x86_64 hardware).
- 

---
##Screeshots <img width="1600" height="900" alt="Image" src="https://github.com/user-attachments/assets/49876f3d-a45d-4bdb-a722-3fd06e6df943" />

## 📝 Notes

- No hardcoded heading logic or document-specific rules.
- No API or internet calls (except frontend-backend communication).
- Works fully offline.

---

## 🏁 Quick Start Table

| Task                | Command/URL                        |
|---------------------|------------------------------------|
| Build backend image | `docker build -t pdf-outline-backend .` |
| Run backend         | `docker run -p 5000:5000 pdf-outline-backend` |
| Start frontend      | `cd frontend && npm install && npm start` |
| Backend API         | http://localhost:5000/extract-outline |
| Frontend UI         | http://localhost:3000               |

---

## 👤 Author

Viyom shukla,Nikhil sharma,utkarsh mishra
