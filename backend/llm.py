from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="your_API_KEY"
)

async def stream_llm(text: str):
    response = client.chat.completions.create(
        model="your_model",
        stream=True,
        messages=[
            {
                "role": "system",
                "content": "You are a realtime AI voice assistant."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
