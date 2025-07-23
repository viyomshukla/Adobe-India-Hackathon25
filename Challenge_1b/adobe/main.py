import json
import re
import spacy
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer, util
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ExtractedSection:
    document: str
    page_number: int
    section_title: str
    importance_rank: int

@dataclass
class SubsectionAnalysis:
    document: str
    refined_text: str
    page_number: int

@dataclass
class DocumentMetadata:
    input_documents: List[str]
    persona: str
    job_to_be_done: str
    processing_timestamp: str

class PersonaProfiler:
    def __init__(self):
        self.persona_keywords = {
            'researcher': ['methodology', 'research', 'analysis', 'study', 'experiment', 'results', 'findings', 'literature', 'review', 'hypothesis', 'data', 'statistical'],
            'student': ['concept', 'definition', 'example', 'theory', 'principle', 'fundamental', 'basic', 'introduction', 'overview', 'summary', 'key points'],
            'analyst': ['trend', 'growth', 'revenue', 'market', 'financial', 'performance', 'metrics', 'KPI', 'analysis', 'forecast', 'strategy', 'competitive'],
            'engineer': ['implementation', 'technical', 'specification', 'design', 'architecture', 'system', 'algorithm', 'optimization', 'performance', 'scalability'],
            'executive': ['summary', 'strategic', 'overview', 'key findings', 'recommendations', 'business impact', 'ROI', 'risk', 'opportunity', 'decision'],
            'travel planner': ['itinerary', 'accommodation', 'restaurant', 'activity', 'attraction', 'transport', 'booking', 'schedule', 'budget', 'location', 'hotel', 'sightseeing', 'tour', 'trip', 'visit', 'experience'],
            'planner': ['plan', 'schedule', 'organize', 'coordinate', 'arrange', 'booking', 'reservation', 'timeline', 'logistics', 'preparation']
        }

    def analyze_persona(self, persona: str) -> Dict[str, Any]:
        persona_lower = persona.lower()
        persona_type = 'general'
        max_match = 0
        for p_type, keywords in self.persona_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in persona_lower)
            if matches > max_match:
                max_match = matches
                persona_type = p_type
        return {
            'type': persona_type,
            'keywords': self.persona_keywords.get(persona_type, []),
        }

class DocumentProcessor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None

    def extract_text_from_pdf(self, pdf_path: str) -> Dict[int, str]:
        page_texts = {}
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                page_texts[page_num + 1] = text
            doc.close()
        except Exception as e:
            logger.error(f"Failed to extract text from {pdf_path}: {e}")
        return page_texts

    def identify_sections(self, text: str) -> List[Dict[str, str]]:
        # Improved: Accepts numbered, ALL CAPS, Title Case, Markdown, and fallback
        patterns = [
            r'^(\d+\.\s*[A-Z][^.]*?)(?:\n|\r\n?)',
            r'^([A-Z][A-Z\s]{3,}?)(?:\n|\r\n?)',
            r'^([A-Z][a-z\s]{5,}?)(?:\n|\r\n?)',
            r'^\*\*([^*]+)\*\*',
            r'^#+\s*([^\n]+)',
        ]
        lines = text.split('\n')
        sections = []
        current_section = None
        current_content = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            is_section = False
            for pattern in patterns:
                match = re.match(pattern, line)
                if match:
                    if current_section and current_content:
                        sections.append({'section_title': current_section, 'content': '\n'.join(current_content)})
                    current_section = match.group(1).strip()
                    current_content = []
                    is_section = True
                    break
            if not is_section:
                current_content.append(line)
        if current_section and current_content:
            sections.append({'section_title': current_section, 'content': '\n'.join(current_content)})
        if not sections and text.strip():
            sections.append({'section_title': 'Full Document', 'content': text})
        return sections

class SemanticRelevanceRanker:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def rank_sections(self, sections: List[Dict], persona_profile: Dict, job_keywords: List[str]) -> List[Dict]:
        if not sections:
            return []
        section_texts = [s['content'] for s in sections]
        query = ' '.join(persona_profile['keywords'] + job_keywords)
        section_embeddings = self.model.encode(section_texts, convert_to_tensor=True)
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(section_embeddings, query_embedding).squeeze().cpu().numpy()
        for i, section in enumerate(sections):
            section['relevance_score'] = similarities[i]
        ranked_sections = sorted(sections, key=lambda x: x['relevance_score'], reverse=True)
        for i, section in enumerate(ranked_sections):
            section['importance_rank'] = i + 1
        return ranked_sections

    def extract_job_keywords(self, job_description: str) -> List[str]:
        words = re.findall(r'\b[a-zA-Z]{3,}\b', job_description.lower())
        return list(set(words))

class DocumentIntelligenceSystem:
    def __init__(self):
        self.persona_profiler = PersonaProfiler()
        self.document_processor = DocumentProcessor()
        self.relevance_ranker = SemanticRelevanceRanker()

    def process_documents(self, pdf_paths: List[str], persona: str, job_to_be_done: str, max_sections: int = 10) -> Dict[str, Any]:
        persona_profile = self.persona_profiler.analyze_persona(persona)
        job_keywords = self.relevance_ranker.extract_job_keywords(job_to_be_done)
        all_sections = []
        subsection_analyses = []
        for pdf_path in pdf_paths:
            page_texts = self.document_processor.extract_text_from_pdf(pdf_path)
            for page_num, text in page_texts.items():
                if not text.strip():
                    continue
                sections = self.document_processor.identify_sections(text)
                for section in sections:
                    if len(section['content'].strip()) < 10:
                        continue
                    section_data = {
                        'document': Path(pdf_path).name,
                        'page_number': page_num,
                        'section_title': section['section_title'],
                        'content': section['content']
                    }
                    all_sections.append(section_data)
                    # Subsection analysis: top 3 sentences containing persona/job keywords
                    sentences = re.split(r'[.!?]+', section['content'])
                    relevant_sentences = [s.strip() for s in sentences if any(k in s.lower() for k in persona_profile['keywords'] + job_keywords) and len(s.strip()) > 20]
                    if relevant_sentences:
                        refined_text = '. '.join(relevant_sentences[:3]) + '.'
                        subsection_analyses.append(SubsectionAnalysis(
                            document=Path(pdf_path).name,
                            refined_text=refined_text,
                            page_number=page_num
                        ))
        ranked_sections = self.relevance_ranker.rank_sections(all_sections, persona_profile, job_keywords)
        top_sections = ranked_sections[:max_sections]
        extracted_sections = [
            {
                'document': s['document'],
                'section_title': s['section_title'],
                'importance_rank': s['importance_rank'],
                'page_number': s['page_number']
            }
            for s in top_sections
        ]
        subsection_analysis_output = [
            {
                'document': a.document,
                'refined_text': a.refined_text,
                'page_number': a.page_number
            }
            for a in subsection_analyses[:20]
        ]
        metadata = DocumentMetadata(
            input_documents=[Path(p).name for p in pdf_paths],
            persona=persona,
            job_to_be_done=job_to_be_done,
            processing_timestamp=datetime.now().isoformat() + 'Z'
        )
        return {
            'metadata': asdict(metadata),
            'extracted_sections': extracted_sections,
            'subsection_analysis': subsection_analysis_output
        }

def main():
    print("\U0001F50D Persona-Driven Document Intelligence System")
    user_dir_path = Path("adobe/input")
    input_json_path = user_dir_path / "input.json"
    pdfs_folder = user_dir_path / "PDF"
    output_json_path = Path("adobe/output/challenge1b_output.json")
    if not input_json_path.exists():
        print(f"\u274C input.json not found in {user_dir_path}")
        return
    if not pdfs_folder.exists() or not pdfs_folder.is_dir():
        print(f"\u274C PDF folder not found in {user_dir_path}")
        return
    with open(input_json_path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    documents = input_data.get('documents', [])
    persona_data = input_data.get('persona', {})
    job_data = input_data.get('job_to_be_done', {})
    pdf_paths = [str(pdfs_folder / doc['filename']) for doc in documents]
    persona = persona_data.get('role', 'General User')
    job_to_be_done = job_data.get('task', 'Extract relevant information')
    system = DocumentIntelligenceSystem()
    result = system.process_documents(pdf_paths, persona, job_to_be_done, max_sections=10)
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\u2705 Output saved to {output_json_path}")

if __name__ == "__main__":
    main() 