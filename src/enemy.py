"""
enemy.py

Handle enemy characters and related actions.
"""

import pygame
from src.settings import Enemy as Enemy_CONFIG, Screen


class Enemy(pygame.sprite.Sprite):
    """Enemy class representing the alien objects."""

    # Image source
    IMAGE_PATH = 'assets/images/enemy.png'

    def __init__(self, x: int, y: int):
        """Initialize the enemy."""
        super().__init__()
        self.image = pygame.image.load(self.IMAGE_PATH).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self):
        """Update enemy position."""
        self.rect.y += Enemy_CONFIG.SPEED
        if self.rect.top > Screen.HEIGHT:
            self.kill()
