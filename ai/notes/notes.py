from openai import OpenAI
import json
import os
from dotenv import load_dotenv
load_dotenv()

class NoteSummarizer:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    @staticmethod
    def analyze(message):
        response = NoteSummarizer.client.responses.create(
            model="gpt-4o",
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "You are a brilliant teacher and subject-matter expert. When the user sends you content from a course module, "
                                "your job is to explain it thoroughly, clearly, and engagingly as if you were tutoring them. "
                                "The goal is not to summarize a task, but to help them deeply understand what the content means.\n\n"
                                "Respond in well-structured **Markdown** and **you are to return it in the **analysis**, and include:\n\n"
                                "1. A **summary** of what the module or material is generally about.\n"
                                "2. A **detailed explanation** of its concepts, broken down clearly.\n"
                                "   - Use **examples** and **analogies** where appropriate.\n"
                                "   - Use bullet points, headings, and highlights to organize complex information.\n"
                                "3. If the content *implies an action or assignment*, you may also:\n"
                                "also include a **slide** that is well-structured and can be rendered using reveal.js. It should be in slides format, for example:\n"
                                "   - Give tips on how to approach it.\n"
                                "Be thorough, kind, and clear. You're here to make learning easier, not just faster. Also add good amount of spacing between the sections and text so it could be readable.\n\n"
                            )
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": f"{message}"
                },
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "module_schema",
                    "schema": {
                        "type": "object",
                        "required": ["analysis"],
                        "properties": {
                            "analysis": {
                                "type": "string",
                                "description": "A thoughtful, detailed explanation with a title in Markdown because it would be rendered in markdown, with analogies, examples, and clear structure. add good amount of spacing between the sections and text so it could be readable. Make it long and interesting to read too"
                            },
                            "slide": {
                                "type": "string",
                                "description": "A thoughtful, detailed explanation in markdown that can be rendered using reveal js, so it should be in slides for example slide1 then content, then slide2 then content, it should be very explanatory and presentable like of the content."
                            }
                        },
                        "additionalProperties": False
                    },
                    "strict": True
                }
            },
            reasoning={},
            tools=[],
            temperature=1,
            max_output_tokens=2048,
            top_p=1,
            store=True
        )

        return json.loads(response.output[0].content[0].text)