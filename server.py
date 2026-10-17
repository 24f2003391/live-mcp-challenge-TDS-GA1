
import hashlib
import os

from mcp.server.fastmcp import FastMCP, Context

EMAIL = "24f2003391@ds.study.iitm.ac.in"

mcp = FastMCP(
    "Live Exam MCP Server",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", "10000")),
)


@mcp.tool()
def solve_challenge(ctx: Context) -> str:
    """Calculate the required hash from the current HTTP challenge header."""

    # Read the headers belonging to THIS tool-call request.
    request = ctx.request_context.request
    headers = request.headers

    challenge = headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    # Normalize the registered email as required.
    normalized_email = EMAIL.strip().lower()

    # Build the exact input string.
    message = f"{challenge}:{normalized_email}"

    # Calculate SHA-256 and convert it to lowercase hexadecimal.
    full_hash = hashlib.sha256(message.encode("utf-8")).hexdigest()

    # Return only the first 16 characters.
    return full_hash[:16]


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
