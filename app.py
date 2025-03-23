import threading  # Used to run the Flask API in a background thread so that it can run concurrently with Streamlit.
import time       # Provides sleep functionality to allow the Flask server time to start.
import streamlit as st  # For building the interactive web UI.
import requests   # To send HTTP requests from the Streamlit UI to the Flask API.
from flask import Flask, request, jsonify  # Flask modules for building the API.
import base64     # For encoding/decoding binary data (used for audio).
import json       # For working with JSON data (e.g., converting dictionaries to JSON strings).

# Import processing modules.
# These modules perform tasks like scraping news, cleaning text, sentiment analysis, etc.
from scraper import fetch_and_scrape_articles  # Fetches and scrapes news articles using NewsAPI and BeautifulSoup.
from preprocessing import clean_text             # Cleans the text by removing HTML tags and unwanted characters.
from sentiment_analysis import analyze_sentiment   # Analyzes text sentiment using NLTK VADER.
from topic_extraction import extract_topics        # Extracts key topics from the text using RAKE.
from comparative_analysis import compare_articles    # Compares articles to find common and unique topics and sentiment counts.
from tts import text_to_speech_hindi               # Converts text to Hindi speech using gTTS.
from openai_agent import get_business_context       # Uses OpenAI's API to refine and improve business insights.


# Helper Functions for Comparative Analysis


def generate_comparative_output(processed_articles, comp_analysis):
    """
    Generates a comparative analysis output that includes:
      - The sentiment distribution.
      - Coverage differences (comparisons between articles with different sentiments).
      - Topic overlap (common and unique topics among articles).
    
    Parameters:
      processed_articles (list): A list of dictionaries for each processed article.
      comp_analysis (dict): A dictionary with basic analysis (sentiment distribution, etc.)
    
    Returns:
      dict: A dictionary with keys "Sentiment Distribution", "Coverage Differences", and "Topic Overlap".
    """
    coverage_differences = []  # List to store comparisons between articles.
    n = len(processed_articles)
    
    # Loop through each pair of articles.
    for i in range(n):
        for j in range(i + 1, n):
            # If two articles have different sentiment labels, create a comparison message.
            if processed_articles[i]["Sentiment"] != processed_articles[j]["Sentiment"]:
                comp_msg = (
                    f"Article {i+1} is {processed_articles[i]['Sentiment']} and focuses on "
                    f"{', '.join(processed_articles[i]['Topics'])}, while Article {j+1} is "
                    f"{processed_articles[j]['Sentiment']} and focuses on "
                    f"{', '.join(processed_articles[j]['Topics'])}."
                )
                impact_msg = "This contrast may affect investor sentiment differently."
                coverage_differences.append({
                    "Comparison": comp_msg,
                    "Impact": impact_msg
                })
    
    # Calculate topic overlap. If there are exactly 2 articles, compute the common and unique topics.
    if n == 2:
        topics1 = set(processed_articles[0]["Topics"])
        topics2 = set(processed_articles[1]["Topics"])
        common = list(topics1.intersection(topics2))
        unique1 = list(topics1 - topics2)
        unique2 = list(topics2 - topics1)
        topic_overlap = {
            "Common Topics": common,
            "Unique Topics in Article 1": unique1,
            "Unique Topics in Article 2": unique2
        }
    else:
        # Otherwise, use the common topics from the basic comparative analysis.
        topic_overlap = {"Common Topics": comp_analysis.get("common_topics", [])}
    
    return {
        "Sentiment Distribution": comp_analysis.get("sentiment_distribution", {}),
        "Coverage Differences": coverage_differences,
        "Topic Overlap": topic_overlap
    }

def final_sentiment_analysis(comp_analysis):
    """
    Provides a final sentiment summary in Hindi based on the sentiment distribution.
    
    Parameters:
      comp_analysis (dict): Dictionary that contains sentiment counts.
    
    Returns:
      str: A Hindi sentence summarizing the overall sentiment.
    """
    distribution = comp_analysis.get("sentiment_distribution", {})
    pos = distribution.get("Positive", 0)
    neg = distribution.get("Negative", 0)
    neu = distribution.get("Neutral", 0)
    total = pos + neg + neu
    
    # If no sentiment data is available, return a default message in Hindi.
    if total == 0:
        return "कोई भावनात्मक डेटा उपलब्ध नहीं है।"
    if pos > neg:
        return "समाचार कवरेज अधिकतर सकारात्मक है, जो संभावित विकास का संकेत देती है।"
    elif neg > pos:
        return "समाचार कवरेज मुख्य रूप से नकारात्मक है, जिसके कारण सावधानी बरतने की आवश्यकता हो सकती है।"
    else:
        return "समाचार कवरेज संतुलित प्रतीत होता है।"


# Helper Function to Trim the Analysis for OpenAI


def trim_analysis(final_output):
    """
    Trims the full final output to include only essential information for the OpenAI agent.
    
    This version only includes:
      - The company name.
      - The sentiment distribution (from the comparative sentiment score).
      - The final sentiment analysis.
    
    Parameters:
      final_output (dict): The complete output dictionary.
    
    Returns:
      dict: A trimmed dictionary with essential fields.
    """
    trimmed = {
        "Company": final_output.get("Company", ""),
        "Sentiment Distribution": final_output.get("Comparative Sentiment Score", {}).get("Sentiment Distribution", {}),
        "Final Sentiment Analysis": final_output.get("Final Sentiment Analysis", "")
    }
    return trimmed


# Flask API Setup: Define /analyze-news Endpoint


# Create a new Flask application instance.
flask_app = Flask(__name__)

@flask_app.route('/analyze-news', methods=['POST'])
def analyze_news():
    """
    This Flask API endpoint does the following:
      1. Receives a POST request with 'query' and 'page_size'.
      2. Uses NewsAPI and BeautifulSoup to fetch and scrape news articles.
      3. Cleans and processes the text, performs sentiment analysis, and extracts topics.
      4. Compares the articles to generate a comparative analysis.
      5. Generates a Hindi sentiment summary and creates Hindi TTS audio.
      6. Trims the analysis and sends it to OpenAI for refined business insights.
      7. Returns the complete output as a JSON response.
    """
    try:
        # Get JSON data from the POST request.
        data = request.get_json()
        query = data.get("query")
        page_size = data.get("page_size", 10)
        
        # Check if a query was provided.
        if not query:
            return jsonify({"error": "Query is required."}), 400
        
        # Use the scraper module to fetch and scrape articles.
        scraped_articles = fetch_and_scrape_articles(query + " news", page_size)
        if not scraped_articles:
            return jsonify({"error": "No articles found or error during scraping."}), 404
        
        processed_articles = []
        # Process each scraped article.
        for article in scraped_articles:
            title = article.get("title", "No title")
            summary = article.get("summary", "No summary")
            content = f"{title}. {summary}"
            
            # Clean the text and perform sentiment analysis and topic extraction.
            cleaned_text_val = clean_text(content)
            sentiment, scores = analyze_sentiment(cleaned_text_val)
            topics = extract_topics(cleaned_text_val, num_topics=3)
            
            # Add the processed article data to our list.
            processed_articles.append({
                "Title": title,
                "Summary": summary,
                "Sentiment": sentiment,
                "Topics": topics,
                "URL": article.get("url", "")
            })
        
        # Perform a basic comparative analysis on the processed articles.
        comp_analysis = compare_articles(processed_articles)
        comparative_output = generate_comparative_output(processed_articles, comp_analysis)
        # Get the final sentiment summary in Hindi.
        final_sent = final_sentiment_analysis(comp_analysis)
        
        # Generate Hindi TTS audio for the final sentiment summary.
        tts_audio_obj = text_to_speech_hindi(final_sent)
        tts_audio_bytes = tts_audio_obj.read()
        tts_audio_b64 = base64.b64encode(tts_audio_bytes).decode('utf-8')
        
        # Build the final output dictionary with all results.
        final_output = {
            "Company": query,
            "Articles": processed_articles,
            "Comparative Sentiment Score": comparative_output,
            "Final Sentiment Analysis": final_sent,
            "Audio": tts_audio_b64  # Base64 encoded MP3 of the Hindi speech.
        }
        
        # Trim the output to reduce token count for the OpenAI agent.
        trimmed_analysis = trim_analysis(final_output)
        analysis_str = json.dumps(trimmed_analysis, indent=2, ensure_ascii=False)
        # Get refined business insights from OpenAI.
        refined_context = get_business_context(analysis_str)
        # Add the refined analysis to the final output.
        final_output["Refined Business Analysis"] = refined_context
        
        # Return the final output as a JSON response.
        return jsonify(final_output)
    except Exception as e:
        # If any error occurs, return the error message in JSON.
        return jsonify({"error": str(e)}), 500

def run_flask():
    """
    Runs the Flask API on port 5000.
    The host is set to 0.0.0.0 so the API is accessible within the container.
    """
    flask_app.run(host="0.0.0.0", port=5000, debug=False)


# Start Flask API in a Background Thread (only once)


# Check if the API has already started using Streamlit's session state.
if "API_STARTED" not in st.session_state:
    # Start the Flask server in a new background thread.
    threading.Thread(target=run_flask, daemon=True).start()
    # Wait a little to allow the Flask server to initialize.
    time.sleep(2)
    st.session_state["API_STARTED"] = True


# Streamlit UI Code


def main():
    """
    Main function for the Streamlit user interface.
    It:
      - Displays input fields for the company/topic and number of articles.
      - Sends a POST request to the Flask API.
      - Displays the JSON output and plays the Hindi TTS audio.
    """
    st.title("News Sentiment & Comparative Analyzer")
    
    # Get user input for the company or topic.
    query = st.text_input("Enter the Company or Topic")
    # Get user input for the number of articles to fetch.
    page_size = st.number_input("Number of Articles", min_value=1, max_value=20, value=10)
    
    # When the user clicks the "Search" button, proceed with the request.
    if st.button("Search"):
        if not query:
            st.error("Please enter a company or topic to search.")
            return
        
        # Create the payload with the query and page size.
        payload = {"query": query, "page_size": page_size}
        # Specify the API endpoint (running on localhost within the container).
        api_url = "http://localhost:5000/analyze-news"
        st.write("Using API endpoint:", api_url)
        
        try:
            # Send a POST request with the payload to the API.
            response = requests.post(api_url, json=payload)
            # If the response is not successful, display an error message.
            if response.status_code != 200:
                try:
                    error_msg = response.json().get("error", "Unknown error occurred.")
                except Exception:
                    error_msg = "Unknown error occurred."
                st.error("Error: " + error_msg)
                return
            
            # Parse the JSON response from the API.
            final_output = response.json()
            # Display the final output as pretty JSON on the Streamlit UI.
            st.json(final_output)
            
            # If audio data is present, decode it from Base64 and play it.
            if final_output.get("Audio"):
                audio_b64 = final_output["Audio"]
                audio_bytes = base64.b64decode(audio_b64)
                st.audio(audio_bytes, format="audio/mp3")
                
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")

# Run the main function when this script is executed.
if __name__ == "__main__":
    main()
