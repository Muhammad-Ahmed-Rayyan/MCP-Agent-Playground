# MCP-Agent-Playground

A hands-on exploration of the Model Context Protocol (MCP) for AI agents. A LangChain agent discovers and calls tools exposed by an MCP server, over the 2026-07-28 MCP specification.

Built as Part B of Task 6 of the Alphatron AI/ML Research Internship (2026).

## Architecture

LangChain Agent -> MCP Client (MCPAdapter / FastMCP) -> MCP Server (FastMCP) -> Tool / Resource -> Result -> Agent

[Insert docs/diagrams/mcp-architecture.png]

## What the server exposes

- Tools: add, multiply, read_approved_file
- Resource: docs://approved/{name}
- Prompt: summarize_note
- Security: file access is restricted to the approved_docs folder, and path traversal attempts are denied

## Project structure

- server.py: MCP server
- test_server.py: quick server check
- client.py: plain MCP client (discovery, tool calls, resources, prompts)
- agent.py: LangChain agent using MCP tools
- approved_docs/: the only files the server may read
- docs/: manual, diagrams, screenshots

## Setup (Windows cmd)

    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    copy .env.example .env

Add your free Google AI Studio key to .env, and set LLM_MODEL to a current Flash-Lite model ID.

## Run

    Terminal 1:  python server.py
    Terminal 2:  python test_server.py
                 python client.py
                 python agent.py

## Example agent trace

[Paste the output of agent.py here]

## Documentation

See docs/MCP_Manual.docx for the full MCP technical manual.