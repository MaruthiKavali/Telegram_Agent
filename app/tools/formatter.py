from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def format_response_with_llm(data: dict) -> str:
    prompt = f"""Summarize the following stock data in a professional tone:

{data}

Focus on LTP, market cap, 52-week range, and last quarter results."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response.choices[0].message.content
