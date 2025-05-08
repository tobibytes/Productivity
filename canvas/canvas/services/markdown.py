from markitdown import MarkItDown
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key="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")
md = MarkItDown(llm_client = client, llm_model="gpt-4o")


def convert_to_markdown(url):
    result =  md.convert(url)
    if result.text_content:
        return result.text_content
    return 'Not Found'
