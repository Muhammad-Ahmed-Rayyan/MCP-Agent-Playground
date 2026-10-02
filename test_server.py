import asyncio

from fastmcp import Client

async def main():
    async with Client("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()
        print("TOOLS:", [t.name for t in tools])

        result = await client.call_tool("add", {"a": 3, "b": 5})
        print("add(3, 5) ->", result.data)

        result = await client.call_tool("read_approved_file", {"name": "welcome.txt"})
        print("read welcome.txt ->", result.data)

        result = await client.call_tool("read_approved_file", {"name": "..\\server.py"})
        print("path traversal attempt ->", result.data)

asyncio.run(main())