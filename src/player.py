# -*- coding: utf-8 -*-
"""
player.py

Player-controlled jet fighter sprite for Jet Fighter.

This module defines the :class:`Player` class, which handles movement,
rendering, and temporary invincibility ("blinking") after being hit.
"""

from __future__ import annotations

import pygame

from src.settings import Screen


class Player(pygame.sprite.Sprite):
    """
    Player jet sprite.

    Attributes:
        IMAGE_PATH (str): Path to the player image file.
        SPEED (int): Horizontal movement speed of the player.
        BLINK_DURATION (int): Duration of blinking invincibility in frames.
        image (pygame.Surface): The current player image.
        rect (pygame.Rect): Rectangle defining position and size.
        blink_timer (int): Remaining frames of invincibility blinking.
        visible (bool): Whether the sprite is currently drawn (for blinking).
    """

    IMAGE_PATH: str = "assets/images/player.png"
    SPEED: int = 6
    BLINK_DURATION: int = Screen.FPS // 6 # 1/6 of a second

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize the player sprite.

        Args:
            x (int): Initial x-coordinate (center).
            y (int): Initial y-coordinate (top).
        """
        super().__init__()
        self.image: pygame.Surface = pygame.image.load(self.IMAGE_PATH).convert_alpha()
        self.rect: pygame.Rect = self.image.get_rect(center=(x, y))

        # Blinking (invincibility) state
        self.blink_timer: int = 0

    # ---------------- Update ----------------
    def update(self, keys: pygame.key.ScancodeWrapper) -> None:
        """
        Update player movement and blinking.

        Args:
            keys (pygame.key.ScancodeWrapper): Current key press states.
        """
        # Movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.SPEED

        # Keep inside screen bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, Screen.WIDTH, Screen.HEIGHT))

        # Handle blinking
        if self.blink_timer > 0:
            self.blink_timer -= 1
            self.image.set_alpha(64)
        else:
            self.image.set_alpha(255)

    # ---------------- Effects ----------------
    def blink(self) -> None:
        """Trigger blinking effect for temporary invincibility."""
        self.blink_timer = self.BLINK_DURATION

    # ---------------- Drawing ----------------
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the player if visible (used in manual rendering scenarios).

        Args:
            surface (pygame.Surface): The surface to draw on.
        """

    def kill(self) -> None:
        """Remove the player from all sprite groups."""
        super().kill()
