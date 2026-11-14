import asyncio

from mcp import Client

from server import initialize, mcp


async def main() -> None:
    initialize()

    async with Client(mcp) as client:
        tools = await client.list_tools()
        names = {tool.name for tool in tools.tools}
        print("Tools:", sorted(names))
        assert {"search_cards", "add_card"} <= names

        found = await client.call_tool("search_cards", {"query": "bias"})
        print("Search before add:", found.content[0].text)
        assert "confirmation bias" in found.content[0].text.lower()

        added = await client.call_tool(
            "add_card",
            {
                "question": "What is a schema?",
                "answer": "A mental framework that organizes knowledge.",
                "source": "Lecture 04",
            },
        )
        print("Added:", added.content[0].text)

        found_again = await client.call_tool("search_cards", {"query": "schema"})
        print("Search after add:", found_again.content[0].text)
        assert "schema" in found_again.content[0].text.lower()

    print("Smoke test passed.")


if __name__ == "__main__":
    asyncio.run(main())
