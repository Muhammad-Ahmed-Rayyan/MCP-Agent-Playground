# Agent–Tool Interaction Flow Diagram

## Purpose
Shows the step-by-step message flow for a real run of agent.py,
where the LangChain agent chains two tool calls (add, then multiply)
to answer a multi-step arithmetic question. Traces the full path:
AI Agent -> MCP Client -> MCP Server -> Tool -> Result -> AI Agent.

## Key points
- Corresponds to agent.py, Question 1: "What is (3+5) multiplied by 12?"
- The agent first calls add(3, 5), receives 8.0, then uses that
  result to call multiply(8, 12), receiving 96.0
- Shows the agent discovering tools via list_tools() before any
  reasoning happens
- This exact run is captured in docs/screenshots/05-agent-trace-full.png
  (or 05a-agent-trace-q1-chaining.png if split)

## Diagram

```mermaid
sequenceDiagram
    actor User
    participant Agent as LangChain Agent<br/>(Qwen3 / OpenRouter)
    participant Client as MCP Client<br/>(MCPAdapter)
    participant Server as MCP Server<br/>(FastMCP)
    participant Tool as Tool Function<br/>(add / multiply)

    User->>Agent: "What is (3+5) multiplied by 12?"
    Agent->>Client: list_tools()
    Client->>Server: tools/list
    Server-->>Client: [add, multiply, read_approved_file]
    Client-->>Agent: available tools + schemas

    Note over Agent: Agent reasons:<br/>needs add, then multiply

    Agent->>Client: call_tool("add", {a:3, b:5})
    Client->>Server: tools/call (add)
    Server->>Tool: execute add(3, 5)
    Tool-->>Server: 8.0
    Server-->>Client: result: 8.0
    Client-->>Agent: ToolMessage(8.0)

    Note over Agent: Agent uses result<br/>to decide next tool call

    Agent->>Client: call_tool("multiply", {a:8, b:12})
    Client->>Server: tools/call (multiply)
    Server->>Tool: execute multiply(8, 12)
    Tool-->>Server: 96.0
    Server-->>Client: result: 96.0
    Client-->>Agent: ToolMessage(96.0)

    Agent-->>User: "(3 + 5) × 12 = 96"
```