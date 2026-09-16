import asyncio
import os

from openai import AsyncOpenAI


async def main():
    api_key = os.getenv("DASHSCOPE_API_KEY")

    if not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY is not set")

    client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    response = await client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {
                "role": "user",
                "content": (
                    "Please explain the architecture of a production-grade "
                    "Enterprise AI Agent platform in detail"
                ),
            }
        ],
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())