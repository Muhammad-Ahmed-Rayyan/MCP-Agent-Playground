import asyncio
import os

from dotenv import load_dotenv
from fastmcp import Client

load_dotenv()
SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000/mcp")


async def main():
    async with Client(SERVER_URL) as client:
        print("=== 1. TOOL DISCOVERY ===")
        for tool in await client.list_tools():
            print(f"- {tool.name}: {tool.description}")

        print("\n=== 2. RESOURCE TEMPLATES ===")
        for template in await client.list_resource_templates():
            print(f"- {template.uriTemplate}")

        print("\n=== 3. PROMPTS ===")
        for prompt in await client.list_prompts():
            print(f"- {prompt.name}: {prompt.description}")

        print("\n=== 4. TOOL CALLING ===")
        result = await client.call_tool("multiply", {"a": 6, "b": 7})
        print("multiply(6, 7) ->", result.data)

        result = await client.call_tool("read_approved_file", {"name": "policy.txt"})
        print("read_approved_file('policy.txt') ->", result.data)

        print("\n=== 5. RESOURCE READ ===")
        contents = await client.read_resource("docs://approved/welcome.txt")
        print("docs://approved/welcome.txt ->", contents[0].text)

        print("\n=== 6. PROMPT TEMPLATE ===")
        prompt = await client.get_prompt("summarize_note", {"name": "welcome.txt"})
        print(prompt.messages[0].content.text)

if __name__ == "__main__":
    asyncio.run(main())