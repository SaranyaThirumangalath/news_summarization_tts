import requests                      # For sending HTTP requests
from bs4 import BeautifulSoup        # For parsing HTML content
import streamlit as st               # For showing errors/messages in Streamlit

# Get the NewsAPI key from the Hugging Face Spaces secrets.
NEWSAPI_KEY = st.secrets.get("NEWSAPI_KEY")
if not NEWSAPI_KEY:
    st.error("Please set your NEWSAPI_KEY in the secrets file.")

def fetch_news_articles(query, page_size=10):
    """
    Uses NewsAPI to fetch a list of news articles based on the query.
    Returns the raw article JSON data.
    
    Parameters:
      query (str): The search term (e.g., "Tesla")
      page_size (int): The number of articles to fetch (default is 10)
    
    How it works:
      1. Sends a GET request to NewsAPI's 'everything' endpoint.
      2. Passes the query, page size, and API key as parameters.
      3. Checks if the request was successful and the API returned status 'ok'.
      4. Returns the list of articles if available.
    """
    # Define the endpoint URL for NewsAPI.
    url = "https://newsapi.org/v2/everything"
    # Set up parameters for the GET request.
    params = {
        "q": query,               # Search query (e.g., "Tesla")
        "pageSize": page_size,    # Number of articles to fetch
        "apiKey": NEWSAPI_KEY,    # API key from secrets
        "sortBy": "relevancy",    # Sort results by relevancy
    }
    try:
        # Send a GET request to the NewsAPI endpoint with the parameters.
        response = requests.get(url, params=params)
        # Use print() to log the raw response text to debug.
        print("NewsAPI response text:", response.text)
        response.raise_for_status()  # Raise an error for bad responses.
        data = response.json()         # Convert the response to JSON.
        # Log the parsed JSON data.
        print("NewsAPI data:", data)
        if data.get("status") != "ok":
            st.error("Error fetching news articles from NewsAPI.")
            return []
        return data.get("articles", [])
    except requests.RequestException as e:
        st.error(f"Error: {e}")
        return []

def scrape_article_page(url):
    """
    Scrapes the given URL using BeautifulSoup to extract the title, summary,
    and optionally other metadata such as the published date.
    Only processes pages with an HTML content type.
    
    Parameters:
      url (str): The URL of the news article.
    
    How it works:
      1. Sends a GET request to the URL with a timeout.
      2. Checks if the content is HTML.
      3. Uses BeautifulSoup to extract the title and summary.
      4. Optionally extracts the publication date.
      5. Returns the scraped data as a dictionary.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        st.warning(f"Error fetching URL {url}: {e}")
        return None

    # Check if the response returns HTML.
    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        st.info(f"Skipping non-HTML content: {url}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    
    # Try to extract the title using common patterns.
    title = None
    if soup.find("meta", property="og:title"):
        title = soup.find("meta", property="og:title").get("content", None)
    if not title and soup.title:
        title = soup.title.string.strip()
    if not title:
        title = "No title found"

    # Extract a summary using meta tags or the first paragraph.
    summary = None
    if soup.find("meta", attrs={"name": "description"}):
        summary = soup.find("meta", attrs={"name": "description"}).get("content", None)
    if not summary and soup.find("meta", property="og:description"):
        summary = soup.find("meta", property="og:description").get("content", None)
    if not summary:
        p = soup.find("p")
        summary = p.get_text(strip=True) if p else "No summary found"

    # Optionally, extract the publication date.
    published = None
    if soup.find("meta", property="article:published_time"):
        published = soup.find("meta", property="article:published_time").get("content", None)
    elif soup.find("time"):
        published = soup.find("time").get("datetime", None) or soup.find("time").get_text(strip=True)

    return {
        "title": title,
        "summary": summary,
        "published": published,
        "url": url
    }

def fetch_and_scrape_articles(query, page_size=10):
    """
    Fetches articles from NewsAPI based on the query, then for each returned article URL,
    uses BeautifulSoup to scrape the page and extract metadata.
    
    Parameters:
      query (str): The search query.
      page_size (int): The number of articles to fetch.
    
    How it works:
      1. Calls 'fetch_news_articles' to get raw articles.
      2. Loops through each article, extracts its URL.
      3. Calls 'scrape_article_page' to extract details.
      4. Returns a list of dictionaries with the scraped article data.
    """
    articles = fetch_news_articles(query, page_size)
    print("Fetched articles count:", len(articles))
    scraped_articles = []
    for art in articles:
        url = art.get("url", "")
        print("Processing URL:", url)
        if url:
            scraped_data = scrape_article_page(url)
            if scraped_data:
                scraped_articles.append(scraped_data)
            else:
                print("Scraping failed for URL:", url)
    print("Total scraped articles count:", len(scraped_articles))
    return scraped_articles