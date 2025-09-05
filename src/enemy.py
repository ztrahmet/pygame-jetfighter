# -*- coding: utf-8 -*-
"""
enemy.py

Enemy sprite for Jet Fighter.

This module defines the :class:`Enemy` class, which represents standard
enemy units that move downward from the top of the screen.
"""

from __future__ import annotations

import pygame

from src.settings import Screen


class Enemy(pygame.sprite.Sprite):
    """
    Enemy sprite that falls from the top of the screen.

    Attributes:
        IMAGE_PATH (str): Path to the enemy image file.
        SPEED (int): Vertical movement speed of the enemy.
        image (pygame.Surface): Current enemy image.
        rect (pygame.Rect): Rectangle defining position and size.
        reached (bool): Whether the enemy has reached the bottom of the screen.
    """

    IMAGE_PATH: str = "assets/images/enemy.png"
    SPEED: int = 3

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize the enemy sprite.

        Args:
            x (int): Initial x-coordinate (center).
            y (int): Initial y-coordinate (top).
        """
        super().__init__()
        self.image: pygame.Surface = pygame.image.load(self.IMAGE_PATH).convert_alpha()
        self.rect: pygame.Rect = self.image.get_rect(center=(x, y))

        # True if the enemy reaches the bottom
        self.reached: bool = False

    # ---------------- Update ----------------
    def update(self) -> None:
        """Move enemy downward and check if it reaches the bottom of the screen."""
        self.rect.y += self.SPEED
        if self.rect.top > Screen.HEIGHT:
            self.reached = True
            # kill is handled in play.py
