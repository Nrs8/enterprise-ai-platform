import asyncio
from openai import AsyncOpenAI


client = AsyncOpenAI(
    api_key="sk-ws-H.EMPMDIX.2pUn.MEQCIDmOk0fCmA9ikofru_EmS_vEFsA_7QzbYpxe4F9Uayq1AiBwR3ItuQa6Cl0tB6ULitNX-xd2m-cvnIT_HR3rBKYK9A",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


async def main():

    response = await client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {
                "role": "user",
                "content": "Please explain the architecture of a production-grade Enterprise AI Agent platform in detail"
            }
        ],
    )

    print(response.choices[0].message.content)


asyncio.run(main())