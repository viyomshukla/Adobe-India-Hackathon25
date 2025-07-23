# Persona-Driven Document Intelligence (Batch Version)

This project processes a set of PDFs and an input.json file to generate a persona-driven analysis as a JSON output. The backend is built with Python and runs as a batch job (no API, no frontend).

---

## Project Structure

```
adobe/
  ├── main.py                  # Core document intelligence logic
  ├── requirements.txt         # Python dependencies
  ├── Dockerfile               # Docker build instructions
  ├── download_models.py       # Model download script
  ├── download_st_model.py     # SentenceTransformer model download
  ├── input/
  │   ├── input.json           # Input configuration (see below)
  │   └── PDF/                 # All PDF files referenced in input.json
  └── output/
      └── challenge1b_output.json  # Output file (created after processing)
```

---

## Usage

### 1. Prepare your files
- Place your `input.json` in `adobe/input/`.
- Place all referenced PDFs in `adobe/input/PDF/`.

Example `input.json`:
```json
{
  "persona": { "role": "Travel Planner" },
  "job_to_be_done": { "task": "Plan a trip of 4 days for a group of 10 college friends." },
  "documents": [
    { "filename": "South of France - Cities.pdf" },
    { "filename": "South of France - Cuisine.pdf" }
  ]
}
```

### 2. Build the Docker image
From the project root:
```sh
docker build -t my-backend-app ./adobe
```

### 3. Run the Docker container (with input/output folders mounted)
Replace `<ABSOLUTE_PATH>` with your full path to the project directory (see below for Windows example):

```sh
docker run \
  -v <ABSOLUTE_PATH>/adobe/input:/app/adobe/input \
  -v <ABSOLUTE_PATH>/adobe/output:/app/adobe/output \
  my-backend-app
```

#### Example for Windows PowerShell
```powershell
docker run -v C:/Users/asus/OneDrive/Desktop/Adobe_Hackathon/Adobe-India-Hackathon25/Challenge_1b/adobe/input:/app/adobe/input -v C:/Users/asus/OneDrive/Desktop/Adobe_Hackathon/Adobe-India-Hackathon25/Challenge_1b/adobe/output:/app/adobe/output my-backend-app
```

### 4. Check the output
- After the container finishes, the results will be in `adobe/output/challenge1b_output.json`.

---

## Notes
- There is **no web API** and **no frontend**. All processing is done in batch mode.
- You can edit `input.json` and add/remove PDFs in the `PDF` folder as needed.
- If you want to change the output location, edit `main.py`.

---

## Troubleshooting
- **No output file?**
  - Make sure you mounted the output folder as shown above.
  - Check Docker logs for errors (e.g., missing models, bad input.json, missing PDFs).
- **Model download issues?**
  - The Dockerfile runs scripts to download required models. Ensure you have internet access during build.

---

## Authors
Viyom Shukla, Nikhil Sharma, Utkarsh Mishra
