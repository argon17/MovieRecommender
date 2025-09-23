import logging
import google.generativeai as genai

class LLMService:
    """Handles interactions with the Google Gemini LLM."""
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("Gemini API key is not configured.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        logging.info("LLMService initialized successfully.")

    def get_movie_recommendation(self, comments):
        """
        Analyzes comments to generate a movie recommendation.
        """
        logging.info("Sending comments to Gemini for analysis...")
        
        prompt = f"""
        You are a movie critic and recommendation expert. Your task is to analyze the following Reddit comments from the past week and generate a "Weekly Movie Buzz" report.

        Based on the collective sentiment, recurring movie titles, and discussions in the comments provided below, please do the following:

        1.  **Identify 1 to 3 movies** that are generating the most positive buzz or interesting discussion.
        2.  For each movie, write a short, compelling paragraph explaining *why* it's being recommended this week, citing the tone of the Reddit discussions (e.g., "users are praising its stunning visuals," "many are debating its controversial ending").
        3.  Format the output clearly in Markdown with a main title, and use bolding for movie titles. Do not include any introductory or concluding sentences outside of the report itself.

        Here are the comments:
        ---
        {comments}
        ---
        """
        try:
            response = self.model.generate_content(prompt)
            logging.info("Successfully received recommendation from Gemini.")
            return response.text
        except Exception as e:
            logging.error(f"Failed to get recommendation from Gemini: {e}")
            return None