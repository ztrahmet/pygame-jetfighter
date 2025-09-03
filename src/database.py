"""
database.py

Handle database operations for the game, including saving and retrieving scores.
"""

from sqlite3 import connect, Connection, Cursor
from typing import List, Tuple # type hints for older Python versions (<3.9)

DB_PATH = 'db/game.db'


class Database:
    """A simple wrapper for SQLite operations for the game."""

    def __init__(self, db_path: str = DB_PATH):
        """
        Initialize the Database instance.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
        self._init_db()

    def _connect(self) -> Connection:
        """Create a connection to the SQLite database."""
        return connect(self.db_path)

    def _init_db(self):
        """Initialize the database and create the scores table if it doesn't exist."""
        with self._connect() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def save_score(self, name: str, score: int):
        """
        Save a player's score to the database.

        Args:
            name (str): Player's name.
            score (int): Player's score.
        """
        with self._connect() as conn:
            conn.execute(
                'INSERT INTO scores (name, score) VALUES (?, ?)',
                (name, score)
            )
            conn.commit()

    def get_high_scores(self, limit: int = 5) -> List[Tuple[str, int, str]]:
        """
        Retrieve the top scores from the database.

        Args:
            limit (int): Number of top scores to return.

        Returns:
            List of tuples: Each tuple contains (name, score, date).
        """
        with self._connect() as conn:
            cursor: Cursor = conn.execute(
                'SELECT name, score, date FROM scores ORDER BY score DESC LIMIT ?',
                (limit,)
            )
            return cursor.fetchall()
