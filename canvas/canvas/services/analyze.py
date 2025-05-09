from openai import OpenAI
import json

client = OpenAI(api_key="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")
def analyze(message):
    response = client.responses.create(
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
                            "Respond in well-structured **Markdown**, and include:\n\n"
                            "1. A **summary** of what the module or material is generally about.\n"
                            "2. A **detailed explanation** of its concepts, broken down clearly.\n"
                            "   - Use **examples** and **analogies** where appropriate.\n"
                            "   - Use bullet points, headings, and highlights to organize complex information.\n"
                            "3. If the content *implies an action or assignment*, you may also:\n"
                            "   - Give tips on how to approach it.\n"
                            "   - Suggest a realistic **priority** (1 = low, 2 = medium, 3 = high).\n"
                            "   - Propose a **completion date**, if appropriate.\n\n"
                            "Be thorough, kind, and clear. You're here to make learning easier, not just faster."
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
                    "required": ["title", "analysis", "priority"],
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "A good title summarizing the concept or module."
                        },
                        "analysis": {
                            "type": "string",
                            "description": "A thoughtful, detailed explanation in Markdown, with analogies, examples, and clear structure."
                        },
                        "priority": {
                            "type": "number",
                            "description": "If relevant, the priority level: 1 = low, 2 = medium, 3 = high."
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