from markitdown import MarkItDown
from openai import OpenAI
import os
import requests
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
md = MarkItDown(llm_client=client, llm_model="gpt-4o")

def convert_to_markdown(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Read content as bytes
        byte_stream = BytesIO(response.content)

        result = md.convert_stream(byte_stream)
        return result.text_content if result.text_content else ''
    except Exception as e:
        print(f"❌ Failed to convert URL: {e}")
        return ''
    