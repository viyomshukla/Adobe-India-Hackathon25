import os
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
import json
from pathlib import Path
from main import DocumentIntelligenceSystem

app = FastAPI()

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze/")
async def analyze(
    input_json: UploadFile = File(...),
    pdfs: List[UploadFile] = File(...)
):
    # Create a temp directory for this request
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        # Save input.json
        input_json_path = tmpdir_path / "input.json"
        with open(input_json_path, "wb") as f:
            f.write(await input_json.read())
        # Create PDFs folder
        pdfs_folder = tmpdir_path / "PDFs"
        pdfs_folder.mkdir(exist_ok=True)
        # Save all PDFs
        for pdf in pdfs:
            pdf_path = pdfs_folder / pdf.filename
            with open(pdf_path, "wb") as f:
                f.write(await pdf.read())
        # Parse input.json to get filenames
        with open(input_json_path, "r", encoding="utf-8") as f:
            input_data = json.load(f)
        documents = input_data.get("documents", [])
        pdf_paths = [str(pdfs_folder / doc["filename"]) for doc in documents]
        persona = input_data.get("persona", {}).get("role", "General User")
        job_to_be_done = input_data.get("job_to_be_done", {}).get("task", "Extract relevant information")
        # Run the intelligence system
        system = DocumentIntelligenceSystem()
        result = system.process_documents(pdf_paths, persona, job_to_be_done, max_sections=10)
        # Save output
        output_json_path = tmpdir_path / "challenge1b_output.json"
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        # Read file into memory and return as a response
        with open(output_json_path, "rb") as f:
            data = f.read()
        return Response(
            content=data,
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=challenge1b_output.json"}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 