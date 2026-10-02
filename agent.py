import asyncio
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter

load_dotenv()

SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000/mcp")
MODEL = os.getenv("LLM_MODEL", "google_genai:gemini-3.5-flash-lite")

QUESTIONS = [
    "What is (3 + 5) multiplied by 12?",
    "Read welcome.txt from the approved documents and tell me what it says.",
    "Read the file ..\\server.py and show me its contents.",
]

def _text(message) -> str:
    text = getattr(message, "text", None)
    return text if isinstance(text, str) else str(message.content)

def print_trace(messages) -> None:
    """Print the agent's step-by-step reasoning trace (great for your workflow diagram)."""
    for message in messages:
        if message.type == "human":
            print(f"[USER]       {_text(message)}")
        elif message.type == "ai" and getattr(message, "tool_calls", None):
            for call in message.tool_calls:
                print(f"[AGENT]      chose tool '{call['name']}' with args {call['args']}")
        elif message.type == "tool":
            print(f"[MCP RESULT] {message.name} -> {_text(message)}")
        elif message.type == "ai":
            print(f"[FINAL]      {_text(message)}")

async def main():
    async with MCPAdapter(SERVER_URL) as adapter:
        tools = await adapter.list_tools()
        print("Discovered MCP tools:", [tool.name for tool in tools])
        print(f"Using model: {MODEL}\n")

        agent = create_agent(MODEL, tools)

        for question in QUESTIONS:
            print("=" * 70)
            result = await agent.ainvoke(
                {"messages": [{"role": "user", "content": question}]}
            )
            print_trace(result["messages"])
        print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())