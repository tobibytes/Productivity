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
                            "You are an expert assistant who explains tasks clearly and patiently, like a great teacher. "
                            "When analyzing the user's message, break it down thoughtfully and explain it in Markdown format. "
                            "Use **analogies**, **step-by-step guidance**, and highlight important concepts using `bold`, `italic`, or bullet points. "
                            "Your response should include:\n\n"
                            "1. A **summary** of what the task is about.\n"
                            "2. An **in-depth explanation** of what it requires, with helpful analogies where possible.\n"
                            "3. **Advice on how to complete the task** efficiently.\n"
                            "4. A suggested **priority** level as an integer:\n"
                            "   - 1 = Low\n"
                            "   - 2 = Medium\n"
                            "   - 3 = High\n"
                            "5. A **recommended date** to complete the task.\n\n"
                            "Use clear, readable Markdown that renders well in any Markdown viewer."
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
                "name": "task_schema",
                "schema": {
                    "type": "object",
                    "required": ["priority", "analysis", "title"],
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "A suitable title for the task."
                        },
                        "analysis": {
                            "type": "string",
                            "description": "A detailed, well-written analysis of the message in Markdown."
                        },
                        "priority": {
                            "type": "number",
                            "description": "Priority level of the task: 1 for low, 2 for medium, and 3 for high."
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