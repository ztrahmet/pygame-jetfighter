#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py

Entry point for the Jet Fighter game.

This module initializes the game application and runs the main loop by
instantiating :class:`src.game.Game`.

The behavior and logic of the game itself live in src/game.py.
This file's purpose is intentionally minimal: start the program.
"""

from __future__ import annotations

from src.game import Game


def main() -> None:
    """
    Create the Game instance and run it.

    This function intentionally performs no additional logic so that
    initialization and teardown are handled by the Game class.
    """
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
