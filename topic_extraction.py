from rake_nltk import Rake
import nltk
import re

# Download stopwords; no need for punkt if we use our own sentence tokenizer.
nltk.download('stopwords', quiet=True)

def simple_sent_tokenize(text):
    """
    A simple sentence tokenizer that splits text on punctuation followed by whitespace.
    """
    # This regex splits on . ! ? followed by one or more spaces.
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return sentences

def extract_topics(text, num_topics=3):
    """
    Extracts key topics from the input text using RAKE (Rapid Automatic Keyword Extraction).
    
    Parameters:
        text (str): The text to analyze.
        num_topics (int): Number of top topics/keywords to return.
        
    Returns:
        list: A list of extracted topics.
    """
    if not text:
        return []
    
    # Use our simple sentence tokenizer to avoid the punkt_tab issue
    r = Rake(sentence_tokenizer=simple_sent_tokenize)
    r.extract_keywords_from_text(text)
    
    ranked_phrases = r.get_ranked_phrases()
    return ranked_phrases[:num_topics] if ranked_phrases else []