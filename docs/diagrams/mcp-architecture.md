# MCP Architecture Diagram

## Purpose
Shows the relationship between the MCP host, client, server, and the
three MCP primitives (tools, resources, prompts) used in this project,
along with the transport layer connecting them.

## Key points
- Host: this project's LangChain agent (Qwen3 via OpenRouter) plus the
  MCP client (MCPAdapter / FastMCP Client)
- Transport: Streamable HTTP, at http://127.0.0.1:8000/mcp
- Server: server.py, built with FastMCP, exposing 3 tools, 1 resource
  template, and 1 prompt
- Security: tool and resource access is restricted to the
  approved_docs/ folder (least-privilege, path validation)

## Diagram

```mermaid
flowchart TB
    subgraph Host["MCP Host (Your Application)"]
        LLM["LLM / LangChain Agent<br/>(Qwen3 via OpenRouter)"]
        Client["MCP Client<br/>(MCPAdapter / FastMCP Client)"]
        LLM <--> Client
    end

    subgraph Transport["Transport Layer"]
        HTTP["Streamable HTTP<br/>(used in this project:<br/>http://127.0.0.1:8000/mcp)"]
        STDIO["stdio<br/>(local subprocess,<br/>not used here)"]
    end

    subgraph Server["MCP Server (server.py — FastMCP)"]
        direction TB
        Tools["Tools<br/>(model-controlled)<br/>add, multiply,<br/>read_approved_file"]
        Resources["Resources<br/>(application-controlled)<br/>docs://approved/{name}"]
        Prompts["Prompts<br/>(user-controlled)<br/>summarize_note"]
    end

    subgraph External["External System"]
        Files["approved_docs/<br/>(sandboxed file access)"]
    end

    Client -->|"1. initialize"| HTTP
    HTTP -->|"2. capability negotiation"| Server
    Client -->|"3. tools/list, resources/list,<br/>prompts/list"| HTTP
    Client -->|"4. tools/call, resources/read,<br/>prompts/get"| HTTP
    HTTP --> Tools
    HTTP --> Resources
    HTTP --> Prompts
    Tools -->|"least-privilege<br/>path validation"| Files
    Resources --> Files

    style Host fill:#1e3a5f,color:#fff
    style Server fill:#2d4a2d,color:#fff
    style External fill:#4a2d2d,color:#fff
    style Transport fill:#3d3d5c,color:#fff
```