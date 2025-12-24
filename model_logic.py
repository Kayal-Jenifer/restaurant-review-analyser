import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load SpaCy for keywords/entities
nlp = spacy.load("en_core_web_sm")
# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

def analyze_review(text):
    # 1. Sentiment Analysis via VADER
    # compound score ranges from -1 to 1
    vs = analyzer.polarity_scores(text)
    compound = vs['compound']
    
    # Normalize -1 to 1 into 0 to 1
    normalized_score = (compound + 1) / 2
    
    # Strict thresholds based on your requirements
    if normalized_score > 0.5:
        label = "Positive"
    elif normalized_score < 0.5:
        label = "Negative"
    else:
        label = "Neutral"

    # 2. Entity & Keyword Extraction
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ"] and not token.is_stop]

    return {
        "score": round(normalized_score, 2),
        "label": label,
        "entities": ", ".join(entities) if entities else "None",
        "keywords": ", ".join(keywords[:5]) if keywords else "None"
    }