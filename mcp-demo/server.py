from contextlib import contextmanager
from pathlib import Path
import sqlite3

from mcp.server.mcpserver import MCPServer

DB_PATH = Path(__file__).with_name("cards.db")
mcp = MCPServer("flashcards-db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    source TEXT NOT NULL DEFAULT ''
)
"""


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute(SCHEMA)
    return connection


@contextmanager
def database():
    db = connect()
    try:
        yield db
        db.commit()
    finally:
        db.close()


def initialize() -> None:
    with database() as db:
        if db.execute("SELECT COUNT(*) FROM cards").fetchone()[0] == 0:
            db.executemany(
                "INSERT INTO cards (question, answer, source) VALUES (?, ?, ?)",
                [
                    (
                        "What is confirmation bias?",
                        "The tendency to notice and trust evidence that supports what you already believe.",
                        "Lecture 03",
                    ),
                    (
                        "What is the anchoring effect?",
                        "The tendency for the first number you see to pull later estimates toward it.",
                        "Lecture 03",
                    ),
                    (
                        "What is the availability heuristic?",
                        "Judging how likely something is by how easily examples come to mind.",
                        "Lecture 03",
                    ),
                ],
            )


@mcp.tool()
def search_cards(query: str, limit: int = 5) -> list[dict]:
    """Search flashcards by question or answer text."""
    pattern = f"%{query}%"
    with database() as db:
        rows = db.execute(
            """
            SELECT id, question, answer, source
            FROM cards
            WHERE question LIKE ? OR answer LIKE ?
            ORDER BY id
            LIMIT ?
            """,
            (pattern, pattern, limit),
        ).fetchall()
    return [dict(row) for row in rows]


@mcp.tool()
def add_card(question: str, answer: str, source: str = "") -> dict:
    """Add a flashcard and return its new id."""
    with database() as db:
        cursor = db.execute(
            "INSERT INTO cards (question, answer, source) VALUES (?, ?, ?)",
            (question, answer, source),
        )
        card_id = cursor.lastrowid
    return {
        "id": card_id,
        "question": question,
        "answer": answer,
        "source": source,
    }


if __name__ == "__main__":
    initialize()
    mcp.run()
