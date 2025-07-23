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

## ⚙️ Approach & Libraries Used

- **PyMuPDF (fitz):** For fast, reliable PDF parsing and text extraction.
- **No ML models:** The solution is heuristic-based (font size, font weight, position) and does not use any large pre-trained models.

---

## ▶️ How to Build and Run the Solution (Batch Processing)

### Prerequisites
- **Docker** (Install from https://www.docker.com/products/docker-desktop/)

### Steps

1. **Place your PDF files** in the `app/input/` directory.
2. **Build the Docker image:**
   ```sh
   cd Adobe_T1
   docker build -t pdf-outline-batch .
   ```
3. **Run the Docker container:**
   ```sh
   docker run --rm -v "$(pwd)/app/input:/app/app/input" -v "$(pwd)/app/output:/app/app/output" pdf-outline-batch
   ```
   - On Windows PowerShell, use:
   ```powershell
   docker run --rm -v ${PWD}/app/input:/app/app/input -v ${PWD}/app/output:/app/app/output pdf-outline-batch
   ```
4. **Results:**
   - For each PDF in `app/input/`, a corresponding `.json` file will be created in `app/output/`.

---

## 📦 Dependencies

- Python 3.10 (handled by Docker)
- PyMuPDF (`fitz`)

All backend dependencies are listed in `requirements.txt`.

---

## 📂 File Structure

```
app/
  input/      # Input PDFs
  output/     # Output JSONs
  main.py     # Batch script
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
- No API or internet calls.
- Works fully offline.
- Heading detection now uses **all pages** of each PDF for improved accuracy on long documents.

---

## 🏁 Quick Start Table

| Task                | Command/URL                        |
|---------------------|------------------------------------|
| Build batch image   | `docker build -t pdf-outline-batch .` |
| Run batch processor | `docker run --rm -v "$(pwd)/app/input:/app/app/input" -v "$(pwd)/app/output:/app/app/output" pdf-outline-batch` |

---

## 👤 Author

Viyom shukla, Nikhil sharma, Utkarsh mishra
