News Sentiment & Comparative Analyzer

Overview

The News Sentiment & Comparative Analyzer is a web-based application that:

  - Extracts key details from news articles related to a given company.
  - Performs sentiment analysis (positive, negative, neutral) on article content.
  - Conducts a comparative analysis to highlight differences in news coverage.
  - Converts the final sentiment analysis into Hindi text-to-speech (TTS) output.
  - Uses an OpenAI agent to refine the business analysis based on the scraped data.

The app provides a user-friendly interface built with Streamlit and is deployed on Hugging Face Spaces.

-------------------------------------------------------------------------------------------------------

Features

  - News Extraction:
     Scrapes at least 10 news articles using NewsAPI and BeautifulSoup.
  
  - Sentiment Analysis:
     Uses NLTK's VADER for sentiment classification.
  
  - Comparative Analysis:
     Computes coverage differences, sentiment distribution, and topic overlaps.
  
  - Text-to-Speech:
     Converts the final sentiment summary into Hindi speech using gTTS.
  
  - OpenAI Integration:
     Refines the analysis by providing business-specific insights.
  
  - API-Based Communication:
     The backend (Flask API) communicates with the frontend (Streamlit) via RESTful endpoints.

-------------------------------------------------------------------------------------------------------

Project Structure

  - app.py                  # Combined Flask API and Streamlit UI
  - scraper.py              # Module for news extraction (using NewsAPI and BeautifulSoup)
  - preprocessing.py        # Module for cleaning text (removes HTML, special characters
  - sentiment_analysis.py   # Module for sentiment analysis using NLTK VADER
  - topic_extraction.py     # Module for extracting key topics using RAKE
  - comparative_analysis.py # Module for performing comparative analysis on articles
  - tts.py                  # Module for converting text to Hindi speech using gTTS
  - openai_agent.py         # Module for refining business analysis using OpenAI's Chat API
  - requirements.txt        # List of dependencies
  - README.md               # Project documentation (this file)

-------------------------------------------------------------------------------------------------------

Installation and Setup

1. Clone the Repository

    git clone https://github.com/username/repo-name.git
    cd repo-name

2. Set Up the Python Environment
    Create and activate a virtual environment:
      python3 -m venv env
      source env/bin/activate  # On Windows: env\Scripts\activate

3. Install Dependencies

    pip install -r requirements.txt

4. Configuration
    Hugging Face Spaces Secrets
    In the Hugging Face Spaces project settings, add the following secret keys:
    - OPENAI_API_KEY – OpenAI API key.

(For local testing, you can set these as environment variables or in a .env file if using a library like python-dotenv.)

-------------------------------------------------------------------------------------------------------

Usage
 
1. Running Locally
   Run the combined app by executing:
    streamlit run app.py

This command starts both the Flask API (in a background thread) and the Streamlit UI. Enter a company name (or topic) and the number of articles, then click Search. The app will display:
    - A structured JSON output with article details.
    - A refined business analysis from the OpenAI agent.
    - A playable Hindi TTS audio file.


2. API Endpoints
  
   POST /analyze-news

   Description:
    Processes the given query, scrapes articles, analyzes sentiment, performs comparative analysis, generates Hindi TTS audio, and returns a structured JSON output.
    Request Body Example:

        {
          "query": "Tesla",
          "page_size": 10
        }

    Request Body Example:

        {
          "Company": "Tesla",
          "Articles": [
            {
              "Title": "Tesla's New Model Breaks Sales Records",
              "Summary": "Tesla's latest EV sees record sales in Q3...",
              "Sentiment": "Positive",
              "Topics": ["Electric Vehicles", "Innovation", "Sales"],
              "URL": "https://example.com/article"
            }
            // ... additional articles ...
          ],
          "Comparative Sentiment Score": {
            "Sentiment Distribution": { "Positive": 6, "Negative": 3, "Neutral": 1 },
            "Coverage Differences": [
              {
                "Comparison": "Article 1 is Positive and focuses on Electric Vehicles, Innovation, Sales, while Article 2 is Negative and focuses on Regulations, Technology, Safety.",
                "Impact": "This contrast may affect investor sentiment differently."
              }
            ],
            "Topic Overlap": { "Common Topics": ["Electric Vehicles"] }
          },
          "Final Sentiment Analysis": "समाचार कवरेज अधिकतर सकारात्मक है, जो संभावित विकास का संकेत देती है।",
          "Audio": "Base64EncodedAudioString",
          "Refined Business Analysis": "Refined insights from OpenAI..."
        }

 -------------------------------------------------------------------------------------------------------
 
 Error Handling
 
  1. Missing Query:
     If the query field is missing:
      - Status Code: 400 Bad Request
      - Response: {"error": "Query is required."}

  2. No Articles Found / Scraping Error:
     If no articles are found or an error occurs during scraping:
      - Status Code: 404 Not Found
      - Response: {"error": "No articles found or error during scraping."}


3. Internal Server Error:
   For any other errors:
    - Status Code: 500 Internal Server Error
    - Response: {"error": "Error message detailing the issue"}

-------------------------------------------------------------------------------------------------------

Deployment on Hugging Face Spaces
 
1. Push Code:
    - Ensure GitHub repository is up-to-date with all files.


2. Create a New Space:
    - Go to Hugging Face Spaces and create a new Space.
    -  Choose Streamlit as the SDK and link GitHub repository.


3. Configure Secrets:
    - Add OPENAI_API_KEY in the Space settings.


4. Deploy:
    - Once deployed, the Space will provide a public URL where users can access app.

-------------------------------------------------------------------------------------------------------
 
Assumptions and Limitations
 
1. Web Scraping:
    - The scraper only processes non-JS pages. If a site relies heavily on JavaScript, it might not be scraped properly.


2. Sentiment Analysis:
    - Uses NLTK VADER, which is tuned for social media and may not capture all nuances in news articles.


3. OpenAI Integration:
    - The refined analysis depends on the quality of the trimmed JSON and the OpenAI model's interpretation.


4. Token Limitations:
    - The JSON sent to OpenAI is trimmed to avoid exceeding the model's maximum context length.

-------------------------------------------------------------------------------------------------------
 
Dependencies
 
    - streamlit
    - requests
    - flask
    - beautifulsoup4
    - nltk
    - rake-nltk
    - gTTS
    - openai
   
     (See requirements.txt for the complete list.)

