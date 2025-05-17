from openai import OpenAI
import json
import os
from dotenv import load_dotenv
load_dotenv()

class FlashCardGenerator:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    @staticmethod
    def generate_flashcards(message):
        response = FlashCardGenerator.client.responses.create(
            model="gpt-4o",
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "You are an expert educator. Your job is to extract key concepts from the student's course material and generate thoughtful, engaging flashcards.\n\n"
                                "Each flashcard should be a JSON object with:\n"
                                "1. A **question** – short, clear, and focused on understanding a concept.\n"
                                "2. An **answer** – complete and educational, not too long, but deep enough to aid memory.\n\n"
                                "Only return JSON, no Markdown or explanation.\n"
                                "Generate at least 5 flashcards based on the content provided.\n"
                            )
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": f"{message}"
                }
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "flashcard_schema",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "flashcards": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "question": {
                                            "type": "string",
                                            "description": "The flashcard question"
                                        },
                                        "answer": {
                                            "type": "string",
                                            "description": "The flashcard answer"
                                        }
                                    },
                                    "required": ["question", "answer"],
                                    "additionalProperties": False   # ✅ This is required!
                                }
                            }
                        },
                        "required": ["flashcards"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            },
            reasoning={},
            tools=[],
            temperature=0.8,
            max_output_tokens=2048,
            top_p=1,
            store=True
        )

        return json.loads(response.output[0].content[0].text)