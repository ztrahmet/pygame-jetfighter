#!/usr/bin/env python3
"""
main.py

Entry point for the game application.
"""

from src.game import Game


def main():
    """Initialize and run the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
