from flask import Flask, request, jsonify
import fitz  # PyMuPDF
from collections import Counter
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- Extraction logic (copied from main.py, adapted for in-memory use) ---
def extract_blocks(page):
    blocks = []
    for b in page.get_text('dict')['blocks']:
        if 'lines' not in b:
            continue
        for l in b['lines']:
            for s in l['spans']:
                blocks.append({
                    'text': s['text'].strip(),
                    'size': s['size'],
                    'flags': s['flags'],
                    'font': s['font'],
                    'bbox': s['bbox'],
                    'origin': (b['bbox'][1], b['bbox'][0]),
                })
    return blocks

def extract_title(doc):
    page = doc[0]
    blocks = extract_blocks(page)
    if not blocks:
        return "Untitled"
    max_size = max(b['size'] for b in blocks)
    candidates = [b['text'] for b in blocks if b['size'] == max_size and len(b['text']) > 3]
    for c in candidates:
        if c:
            return c
    return "Untitled"

def detect_heading_levels(doc, max_pages=5):
    sizes = []
    for i in range(min(max_pages, len(doc))):
        blocks = extract_blocks(doc[i])
        sizes.extend([b['size'] for b in blocks if len(b['text']) > 3])
    counter = Counter(sizes)
    most_common = [s for s, _ in counter.most_common(5)]
    if not most_common:
        return {}
    levels = {}
    for idx, s in enumerate(sorted(most_common, reverse=True)[:3]):
        levels[s] = f"H{idx+1}"
    return levels

def extract_outline_from_bytes(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    title = extract_title(doc)
    heading_sizes = detect_heading_levels(doc)
    outline = []
    # Only process the first 50 pages (1-based)
    max_pages = min(50, len(doc))
    for page_num in range(1, max_pages + 1):
        page = doc[page_num - 1]
        blocks = extract_blocks(page)
        for b in blocks:
            if b['size'] in heading_sizes and len(b['text']) > 3:
                outline.append({
                    'level': heading_sizes[b['size']],
                    'text': b['text'],
                    'page': page_num
                })
    return {
        'title': title,
        'outline': outline
    }

# --- API endpoint ---
@app.route('/extract-outline', methods=['POST'])
def extract_outline_api():
    if 'files' not in request.files:
        return jsonify({'error': 'No files part in the request'}), 400
    files = request.files.getlist('files')
    results = {}
    for file in files:
        if file.filename.lower().endswith('.pdf'):
            pdf_bytes = file.read()
            outline = extract_outline_from_bytes(pdf_bytes)
            results[file.filename] = outline
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)