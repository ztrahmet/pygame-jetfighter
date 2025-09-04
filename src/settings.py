"""
settings.py

Global configuration constants for the game, including screen, player, and enemy settings.
"""


class Screen:
    """Screen configuration constants."""
    WIDTH = 800
    HEIGHT = 600
    FPS = 60
    BACKGROUND_IMAGE = 'assets/images/background.png'


class Game:
    """Game configuration constants."""
    DIFFICULTY = 'Normal'
    HEART = 3
    MISSILES = 5


class Player:
    """Player configuration constants."""
    SPEED = 6
    MISSILE_SPEED = 7


class Enemy:
    """Enemy configuration constants."""
    SPEED = 3
