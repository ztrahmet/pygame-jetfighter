"""
missile.py

Handle missile behavior and related actions.
"""

import pygame
from src.settings import Player


class Missile(pygame.sprite.Sprite):
    """Missile class representing the player's missiles."""

    def __init__(self, x: int, y: int):
        """Initialize the missile."""
        super().__init__()
        self.image = pygame.image.load('assets/images/missile.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self):
        """Update missile position."""
        self.rect.y -= Player.MISSILE_SPEED
        if self.rect.bottom < 0:
            self.kill()
