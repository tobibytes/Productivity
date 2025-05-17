from openai import OpenAI
import json
import os
from dotenv import load_dotenv
import numpy as np
load_dotenv()

class EmbeddingService:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    @staticmethod
    def split_text(text, max_length=300):
        """
        Split the text into chunks of a specified maximum length.
        
        Args:
            text (str): The text to split.
            max_length (int): The maximum length of each chunk.
        
        Returns:
            list: A list of text chunks.
        """
        words = text.split()
        chunks = []
        current_chunk = []

        for word in words:
            if len(" ".join(current_chunk + [word])) <= max_length:
                current_chunk.append(word)
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks
        
    
    @staticmethod
    def generate_embeddings(text):
        """
        Generate embeddings for the given text using OpenAI's API.
        
        Args:
            text (str): The text to generate embeddings for.
        
        Returns:
            list: The generated embeddings.
        """
        try:
            response = EmbeddingService.client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            
            return np.array(response.data[0].embedding, dtype=np.float32)
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return None