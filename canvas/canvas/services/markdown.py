from markitdown import MarkItDown
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
md = MarkItDown(llm_client = client, llm_model="gpt-4o")


def convert_to_markdown(url):
    result =  md.convert(url)
    if result.text_content:
        return result.text_content
    return 'Not Found'
