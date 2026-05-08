import os

from openai import OpenAI

from AI.services.prompts import SYSTEM_PROMPT

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def ask_ai(question, context):

    response = client.chat.completions.create(

        model="qwen/qwen3-32b:free",

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": f"""

                CONTEXT:
                {context}

                QUESTION:
                {question}

                """
            }
        ],

        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content