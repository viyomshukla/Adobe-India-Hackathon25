import spacy
from sentence_transformers import SentenceTransformer

# Download spaCy model
spacy.cli.download("en_core_web_sm")

# Download sentence-transformers model (will be cached)
SentenceTransformer('all-MiniLM-L6-v2')