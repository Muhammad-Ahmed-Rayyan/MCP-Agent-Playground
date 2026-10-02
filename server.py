from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP("Task6-Demo-Server")

# Only files inside this folder can ever be read (security: least privilege)
APPROVED_DIR = (Path(__file__).parent / "approved_docs").resolve()


def _safe_read(name: str) -> str:
    """Read a .txt file from the approved folder only."""
    target = (APPROVED_DIR / name).resolve()
    if APPROVED_DIR not in target.parents or target.suffix != ".txt":
        return "Access denied: file is not in the approved folder."
    if not target.exists():
        return f"File not found: {name}"
    return target.read_text(encoding="utf-8")

@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers and return the sum."""
    return a + b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the product."""
    return a * b


@mcp.tool()
def read_approved_file(name: str) -> str:
    """Read a text file (e.g. 'welcome.txt') from the approved documents folder."""
    return _safe_read(name)

@mcp.resource("docs://approved/{name}")
def approved_doc(name: str) -> str:
    """An approved document exposed as a read-only resource."""
    return _safe_read(name)

@mcp.prompt()
def summarize_note(name: str) -> str:
    """Prompt template asking the model to summarize an approved note."""
    return f"Read the approved file '{name}' and summarize it in two sentences."


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)