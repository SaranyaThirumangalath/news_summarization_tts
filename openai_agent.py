import streamlit as st
import openai

# Retrieve the API key from Hugging Face Spaces secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_business_context(analysis_json_str):
    """
    Sends the aggregated analysis JSON (as a string) to OpenAI and returns a refined, business-specific analysis.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or another model of your choice
        messages=[
            {
                "role": "system", 
                "content": "You are an expert business analyst specializing in news sentiment analysis. Your role is to review aggregated data from news articles, understand competitor dynamics and market trends, and provide refined, actionable business insights."
            },
            {
                "role": "user", 
                "content": ("Based on the following JSON output from our news sentiment analysis tool, "
                            "please provide a comprehensive business-specific analysis. Include insights on competitor impact, "
                            "market trends, and strategic recommendations for the company. Here is the data:\n\n" + analysis_json_str)
            }
        ],
        temperature=0.7,
        max_tokens=300,
    )
    refined_summary = response.choices[0].message['content'].strip()
    return refined_summary