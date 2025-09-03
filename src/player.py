"""
player.py

Handle player character and related actions.
"""

import pygame
from src.settings import Player as Player_CONFIG


class Player(pygame.sprite.Sprite):
    """Player class representing the jet fighter."""

    def __init__(self, x: int, y: int):
        """Initialize the player."""
        super().__init__()
        self.image = pygame.image.load('assets/images/player.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self, keys):
        """Update player position based on key presses."""
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= Player_CONFIG.SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += Player_CONFIG.SPEED
