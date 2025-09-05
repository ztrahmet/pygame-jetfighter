# -*- coding: utf-8 -*-
"""
boss.py

Special boss enemy sprite for Jet Fighter.

This module defines the :class:`Boss` class, which inherits from
:class:`Enemy` but uses a different sprite to represent a larger,
rarer, and more rewarding enemy.
"""

from __future__ import annotations

import pygame

from src.enemy import Enemy


class Boss(Enemy):
    """
    Boss enemy sprite.

    Inherits from :class:`Enemy`, but uses a different image. Bosses
    appear rarely and grant bonus rewards when destroyed.
    """

    IMAGE_PATH: str = "assets/images/boss.png"

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize the boss enemy sprite.

        Args:
            x (int): Initial x-coordinate (center).
            y (int): Initial y-coordinate (top).
        """
        super().__init__(x, y)
        self.image: pygame.Surface = pygame.image.load(self.IMAGE_PATH).convert_alpha()
        self.rect: pygame.Rect = self.image.get_rect(center=(x, y))
