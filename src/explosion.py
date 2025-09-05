# -*- coding: utf-8 -*-
"""
explosion.py

Explosion sprite for Jet Fighter.

This module defines the :class:`Explosion` class, which represents a
temporary visual and audio effect when enemies or missiles are destroyed.
"""

from __future__ import annotations

import pygame
from src.settings import Screen


class Explosion(pygame.sprite.Sprite):
    """
    Explosion sprite with sound and limited lifetime.

    Attributes:
        IMAGE_PATH (str): Path to the explosion image file.
        SOUND_PATH (str): Path to the explosion sound effect.
        DURATION (int): Lifetime of the explosion in frames.
        image (pygame.Surface): Current explosion image.
        rect (pygame.Rect): Rectangle defining position and size.
        timer (int): Remaining frames before the explosion disappears.
    """

    IMAGE_PATH: str = "assets/images/explosion.png"
    SOUND_PATH: str = "assets/sounds/explosion.wav"
    DURATION: int = Screen.FPS // 5  # frames to stay visible (0.2s)

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize the explosion sprite.

        Args:
            x (int): Initial x-coordinate (center).
            y (int): Initial y-coordinate (top).
        """
        super().__init__()
        self.image: pygame.Surface = pygame.image.load(self.IMAGE_PATH).convert_alpha()
        self.rect: pygame.Rect = self.image.get_rect(center=(x, y))
        self.timer: int = self.DURATION

        # Play explosion sound effect
        try:
            explosion_sound = pygame.mixer.Sound(self.SOUND_PATH)
            explosion_sound.play()
        except pygame.error:
            # If sound file missing or mixer not initialized, ignore gracefully
            pass

    # ---------------- Update ----------------
    def update(self) -> None:
        """Countdown timer and remove explosion after duration ends."""
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
