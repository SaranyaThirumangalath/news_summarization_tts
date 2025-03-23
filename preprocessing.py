import re                         # Import the regular expressions module for pattern matching and text substitution.
from bs4 import BeautifulSoup     # Import BeautifulSoup to parse HTML content.

def clean_text(text):
    """
    Cleans the input text by removing HTML tags, special characters, and extra whitespace.
    
    Parameters:
        text (str): The text to clean.
        
    Returns:
        str: The cleaned text.
    """
    # If the text is empty or None, return an empty string immediately.
    if not text:
        return ""
    
    # Create a BeautifulSoup object to parse the text as HTML.
    # This will help remove any HTML tags present in the text.
    soup = BeautifulSoup(text, "html.parser")
    
    # Get the plain text from the BeautifulSoup object.
    # This step strips out all HTML tags and returns only the text content.
    cleaned = soup.get_text()
    
    # Use a regular expression (regex) to remove characters that are not:
    # - Uppercase (A-Z) or lowercase (a-z) letters,
    # - Numbers (0-9),
    # - Whitespace characters (spaces, tabs, etc.),
    # - Basic punctuation (.,!?'-)
    #
    # The pattern r"[^a-zA-Z0-9\s.,!?'-]" means "match any character that is NOT
    # one of the allowed characters", and re.sub() replaces them with an empty string.
    cleaned = re.sub(r"[^a-zA-Z0-9\s.,!?'-]", "", cleaned)
    
    # Use another regex to replace multiple whitespace characters with a single space.
    # The pattern r'\s+' matches one or more whitespace characters.
    # .strip() removes any leading or trailing whitespace.
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Return the final cleaned text.
    return cleaned
