"""
database.py

Handle database operations for the game, including saving and retrieving scores.
"""

from os import makedirs, path
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
        # Create db folder if it doesn't exist
        db_dir = path.dirname(self.db_path)
        if not path.exists(db_dir):
            makedirs(db_dir)

        # Create scores table if it doesn't exist
        with self._connect() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    score INTEGER NOT NULL,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def save_score(self, score: int):
        """
        Save a player's score to the database.

        Args:
            score (int): Player's score.
        """
        with self._connect() as conn:
            conn.execute(
                'INSERT INTO scores (score) VALUES (?)',
                (score,)
            )
            conn.commit()

            # Check the number of entries and delete the lowest score if exceeding 100
            cursor: Cursor = conn.execute('SELECT COUNT(*) FROM scores')
            total_rows = cursor.fetchone()[0]

            if total_rows > 100:
                # Delete the exstra rows
                conn.execute('''
                    DELETE FROM scores
                    WHERE id IN (
                        SELECT id FROM scores
                        ORDER BY score ASC, date ASC
                        LIMIT ?
                    )
                ''', (total_rows - 100,))
                conn.commit()

    def get_high_scores(self, limit: int = 5) -> List[Tuple[str, int, str]]:
        """
        Retrieve the top scores from the database.

        Args:
            limit (int): Number of top scores to return.

        Returns:
            List of tuples: Each tuple contains (score, date).
        """
        with self._connect() as conn:
            cursor: Cursor = conn.execute(
                'SELECT score, date FROM scores ORDER BY score DESC LIMIT ?',
                (limit,)
            )
            return cursor.fetchall()
