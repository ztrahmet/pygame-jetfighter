# -*- coding: utf-8 -*-
"""
database.py

SQLite-based database management for Jet Fighter.

This module defines the :class:`Database` class, which is responsible for
storing and retrieving game scores. It ensures the database and schema exist,
and provides methods for saving new scores and fetching high scores.

The database is stored in ``db/game.db`` and is kept lightweight.
"""

from __future__ import annotations

import os
import sqlite3
from typing import List, Tuple


class Database:
    """
    Handle database operations for Jet Fighter scores.

    Attributes:
        DB_DIR (str): Directory path for the database file.
        DB_FILE (str): Full file path for the SQLite database.
    """

    DB_DIR: str = "db"
    DB_FILE: str = os.path.join(DB_DIR, "game.db")

    def __init__(self) -> None:
        """Initialize the database and create the scores table if needed."""
        os.makedirs(self.DB_DIR, exist_ok=True)
        self.create_table()

    # ---------------- Table setup ----------------
    def create_table(self) -> None:
        """Create the ``scores`` table if it does not already exist."""
        with sqlite3.connect(self.DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    score INTEGER NOT NULL,
                    difficulty TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    # ---------------- Save score ----------------
    def save_score(self, score: int, difficulty: str) -> None:
        """
        Insert a new score into the database.

        Args:
            score (int): The player's final score.
            difficulty (str): The difficulty setting at which the score was earned.
        """
        with sqlite3.connect(self.DB_FILE) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO scores (score, difficulty)
                VALUES (?, ?)
                """,
                (score, difficulty),
            )
            conn.commit()

            # Keep only the latest 100 scores
            cursor.execute("SELECT COUNT(*) FROM scores")
            count = cursor.fetchone()[0]
            if count > 100:
                cursor.execute(
                    """
                    DELETE FROM scores
                    WHERE id IN (
                        SELECT id FROM scores
                        ORDER BY created_at ASC
                        LIMIT ?
                    )
                    """,
                    (count - 100,),
                )
                conn.commit()

    # ---------------- High scores ----------------
    def get_high_scores(self, limit: int = 5) -> List[Tuple[int, str, str]]:
        """
        Retrieve the top high scores.

        Args:
            limit (int): Maximum number of high scores to return.

        Returns:
            list[tuple[int, str, str]]: List of (score, difficulty, created_at).
        """
        with sqlite3.connect(self.DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT score, difficulty, created_at
                FROM scores
                ORDER BY score DESC
                LIMIT ?
                """,
                (limit,)
            )
            return cursor.fetchall()
