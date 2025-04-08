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
            "text": "analyze this message and return a summary of it, don't make it to long, advise on how to complete the task., also the priority as either low, medium or high as 1,2,3 respectively. the advice and summary should be written in markdown, highlight important things to note so when i render it or copy it to a markdown editor, it will look good .  also put a date it should be completed by."
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
            "required": [
            "priority",
            "due_date",
            "summary",
            "title",
            "from",
            "advice",
            "resources"
            ],
            "properties": {
            "from": {
                "type": "string",
                "description": "The sender of the message, e.g., Canvas or another service."
            },
            "title": {
                "type": "string",
                "description": "A suitable title for the task."
            },
            "advice": {
                "type": "string",
                "description": "Advice on how to complete the task or any relevant guidance. written in markdown"
            },
            "summary": {
                "type": "string",
                "description": "A summary of the message being sent, written in Markdown."
            },
            "due_date": {
                "type": "string",
                "description": "The date by which the task should be completed."
            },
            "priority": {
                "type": "number",
                "description": "Priority level of the task: 1 for low, 2 for medium, and 3 for high."
            },
            "resources": {
                "type": "array",
                "items": {
                "type": "string"
                },
                "description": "A list of resources, such as links, related to the task."
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
