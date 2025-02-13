# utils/nlp_processing.py
import spacy
from spacy.cli import download

MODEL_NAME = "xx_ent_wiki_sm"

try:
    nlp = spacy.load(MODEL_NAME)
except OSError:
    print(f"Model {MODEL_NAME} bulunamadı. İndiriliyor...")
    download(MODEL_NAME)
    nlp = spacy.load(MODEL_NAME)

def process_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def summarize_text(text, max_sentences=3):
    sentences = text.split('. ')
    summary = '. '.join(sentences[:max_sentences])
    return summary
