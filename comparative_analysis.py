def compare_articles(articles):
    """
    Performs comparative analysis on a list of articles.
    Each article in the list should be a dictionary that includes:
      - "sentiment": a string ("Positive", "Negative", or "Neutral")
      - "topics": a list of extracted topic strings
    Returns a dictionary containing:
      - sentiment_distribution: A count of articles by sentiment.
      - common_topics: A list of topics that appear in more than one article.
      - unique_topics: A list of topics that appear in only one article.
    """
    # Initialize a dictionary to count the number of articles for each sentiment.
    sentiment_distribution = {"Positive": 0, "Negative": 0, "Neutral": 0}
    
    # Initialize a dictionary to count how many times each topic appears.
    topic_freq = {}
    
    # Loop over each article in the articles list.
    for article in articles:
        # Get the sentiment of the article, defaulting to "Neutral" if not provided.
        sentiment = article.get("sentiment", "Neutral")
        
        # Increase the count for this sentiment in the sentiment_distribution dictionary.
        if sentiment in sentiment_distribution:
            sentiment_distribution[sentiment] += 1
        else:
            # If the sentiment is not already in the dictionary, add it.
            sentiment_distribution[sentiment] = 1
        
        # Get the list of topics for this article. If not available, use an empty list.
        for topic in article.get("topics", []):
            # Increase the count for each topic in the topic_freq dictionary.
            topic_freq[topic] = topic_freq.get(topic, 0) + 1
    
    # Create a list of common topics that appear in at least 2 articles.
    common_topics = [topic for topic, count in topic_freq.items() if count > 1]
    
    # Create a list of unique topics that appear in only 1 article.
    unique_topics = [topic for topic, count in topic_freq.items() if count == 1]
    
    # Return the results as a dictionary.
    return {
        "sentiment_distribution": sentiment_distribution,
        "common_topics": common_topics,
        "unique_topics": unique_topics,
    }
