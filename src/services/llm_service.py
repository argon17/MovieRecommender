import logging
from typing import Optional
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

class LLMService:
    """Handles interactions with the Google Gemini LLM."""
    def __init__(self, api_key: str) -> None:
        """
        Initialize the LLM service with API key.

        Args:
            api_key: Google Gemini API key

        Raises:
            ValueError: If the API key is not provided
        """
        if not api_key:
            raise ValueError("Gemini API key is not configured.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        logging.info("LLMService initialized successfully.")

    def get_movie_recommendation(self, comments: str) -> Optional[str]:
        """
        Analyzes comments to generate a movie recommendation.

        Args:
            comments: String containing Reddit comments to analyze

        Returns:
            A formatted movie recommendation string, or None if an error occurs
        """
        logging.info("Sending comments to Gemini for analysis...")
        
        prompt = f"""
        You are a seasoned movie critic and recommendation expert. Analyze the following Reddit comments from the past week and generate a "Weekly Movie Buzz" report.  

        Your task is to synthesize the collective voice of Reddit discussions into a clear, engaging digest for movie fans. Focus on movies that stand out based on the comments, whether due to excitement, praise, debate, or controversy.  

        ### Instructions:
        1. **Identify 1 to 3 movies** that generated the most attention this week.  
        - Prioritize movies mentioned frequently, receiving strong positive sentiment, or sparking interesting debate.  
        - If there is a balance of hype and criticism, capture both perspectives.  

        2. For each chosen movie:  
        - Create a **subheading with the movie title in bold**.  
        - Write a **short but rich paragraph (3–5 sentences)** explaining why this movie is recommended or noteworthy this week.  
        - Reference the Reddit buzz directly — highlight what people are saying (e.g., “users loved the soundtrack,” “some found the pacing slow but praised the lead performance”).  
        - Be specific about aspects like performances, direction, visuals, themes, or emotional impact.  

        3. **Formatting requirements:**  
        - Use Markdown.  
        - Include a main title: `# Weekly Movie Buzz`.  
        - Use `##` for each movie subheading.  
        - Do not add an introduction or conclusion outside of the report.  

        Here are the comments to analyze:  
        ---  
        {comments}  
        ---  

        """
        try:
            response = self.model.generate_content(prompt)
            logging.info("Successfully received recommendation from Gemini.")
            return response.text
        except GoogleAPIError as e:
            logging.error("Failed to get recommendation from Gemini: %s", e)
            return None
