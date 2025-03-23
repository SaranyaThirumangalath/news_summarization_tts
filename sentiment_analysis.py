import nltk                              # Import the Natural Language Toolkit for NLP tasks
from nltk.sentiment.vader import SentimentIntensityAnalyzer  # Import VADER, a rule-based sentiment analysis tool

# Download the VADER lexicon if it is not already downloaded.
# The 'quiet=True' option suppresses verbose output.
nltk.download('vader_lexicon', quiet=True)

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the input text using VADER.
    
    Parameters:
        text (str): The text to analyze.
        
    Returns:
        tuple: A tuple containing:
            - sentiment_label (str): "Positive", "Negative", or "Neutral".
            - sentiment_scores (dict): A dictionary with scores for various sentiment metrics.
    """
    # Create an instance of the SentimentIntensityAnalyzer.
    sia = SentimentIntensityAnalyzer()
    
    # Use the analyzer to get sentiment scores for the given text.
    # The 'polarity_scores' method returns a dictionary with:
    # 'neg' (negative), 'neu' (neutral), 'pos' (positive), and 'compound' (an overall score)
    scores = sia.polarity_scores(text)
    
    # The 'compound' score is a single score that sums up the overall sentiment.
    compound = scores['compound']
    
    # Determine the sentiment based on the compound score.
    # A compound score >= 0.05 is considered Positive.
    if compound >= 0.05:
        sentiment = "Positive"
    # A compound score <= -0.05 is considered Negative.
    elif compound <= -0.05:
        sentiment = "Negative"
    # Scores between -0.05 and 0.05 are considered Neutral.
    else:
        sentiment = "Neutral"
        
    # Return the sentiment label along with the full sentiment scores.
    return sentiment, scores
