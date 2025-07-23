import os
import json
import fitz  # PyMuPDF
from collections import Counter, defaultdict

INPUT_DIR = os.path.join(os.path.dirname(__file__), 'input')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')

# Helper: Get all PDF files in input dir
def get_pdf_files(input_dir):
    return [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]

# Helper: Extract text blocks with font info from a page
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
                    'origin': (b['bbox'][1], b['bbox'][0]),  # y, x
                })
    return blocks

# Helper: Guess title from first page (largest text)
def extract_title(doc):
    page = doc[0]
    blocks = extract_blocks(page)
    if not blocks:
        return "Untitled"
    # Find the largest font size
    max_size = max(b['size'] for b in blocks)
    candidates = [b['text'] for b in blocks if b['size'] == max_size and len(b['text']) > 3]
    # Return the first non-empty candidate
    for c in candidates:
        if c:
            return c
    return "Untitled"

# Helper: Detect heading levels by font size clustering
def detect_heading_levels(doc):
    sizes = []
    for i in range(len(doc)):
        blocks = extract_blocks(doc[i])
        sizes.extend([b['size'] for b in blocks if len(b['text']) > 3])
    # Get the most common font sizes
    counter = Counter(sizes)
    most_common = [s for s, _ in counter.most_common(5)]
    if not most_common:
        return {}
    # Assign H1, H2, H3 to the largest three sizes
    levels = {}
    for idx, s in enumerate(sorted(most_common, reverse=True)[:3]):
        levels[s] = f"H{idx+1}"
    return levels

# Main extraction logic
def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    title = extract_title(doc)
    heading_sizes = detect_heading_levels(doc)
    outline = []
    for page_num, page in enumerate(doc, 1):
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

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_files = get_pdf_files(INPUT_DIR)
    for pdf in pdf_files:
        pdf_path = os.path.join(INPUT_DIR, pdf)
        result = extract_outline(pdf_path)
        out_name = os.path.splitext(pdf)[0] + '.json'
        out_path = os.path.join(OUTPUT_DIR, out_name)
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main() 