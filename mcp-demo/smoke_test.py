import asyncio
import tempfile
from pathlib import Path

from mcp import Client

import server


def result_text(result, label: str) -> str:
    assert not result.is_error, f"{label} failed: {result.content}"
    assert result.content, f"{label} returned no content"
    return result.content[0].text


async def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        server.DB_PATH = Path(tmp) / "cards.db"
        server.initialize()

        async with Client(server.mcp) as client:
            tools = await client.list_tools()
            names = {tool.name for tool in tools.tools}
            print("Tools:", sorted(names))
            assert {"search_cards", "add_card"} <= names

            found = await client.call_tool("search_cards", {"query": "bias"})
            found_text = result_text(found, "search before add")
            print("Search before add:", found_text)
            assert "confirmation bias" in found_text.lower()

            added = await client.call_tool(
                "add_card",
                {
                    "question": "What is a schema?",
                    "answer": "A mental framework that organizes knowledge.",
                    "source": "Lecture 04",
                },
            )
            print("Added:", result_text(added, "add card"))

            found_again = await client.call_tool("search_cards", {"query": "schema"})
            found_again_text = result_text(found_again, "search after add")
            print("Search after add:", found_again_text)
            assert "schema" in found_again_text.lower()

    print("Smoke test passed.")


if __name__ == "__main__":
    asyncio.run(main())
