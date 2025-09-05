# -*- coding: utf-8 -*-
"""
missile.py

Missile sprite for Jet Fighter.

This module defines the :class:`Missile` class, which represents
the player's fired projectiles that travel upward and can hit enemies.
"""

from __future__ import annotations

import pygame


class Missile(pygame.sprite.Sprite):
    """
    Player missile sprite.

    Attributes:
        IMAGE_PATH (str): Path to the missile image file.
        SPEED (int): Vertical speed of the missile (moves upward).
        image (pygame.Surface): Current missile image.
        rect (pygame.Rect): Rectangle defining position and size.
    """

    IMAGE_PATH: str = "assets/images/missile.png"
    SPEED: int = 7

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize the missile sprite.

        Args:
            x (int): Initial x-coordinate (center).
            y (int): Initial y-coordinate (top).
        """
        super().__init__()
        self.image: pygame.Surface = pygame.image.load(self.IMAGE_PATH).convert_alpha()
        self.rect: pygame.Rect = self.image.get_rect(center=(x, y))

    # ---------------- Update ----------------
    def update(self) -> None:
        """Move the missile upward and remove it if it leaves the screen."""
        self.rect.y -= self.SPEED
        if self.rect.bottom < 0:
            self.kill()
