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

    # Enemy configuration
    SPEED = Enemy_CONFIG.SPEED

    def __init__(self, x: int, y: int):
        """Initialize the enemy."""
        super().__init__()
        self.image = pygame.image.load(self.IMAGE_PATH).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.reached = False
    
    def update(self):
        """Update enemy position."""
        self.rect.y += self.SPEED
        if self.rect.top > Screen.HEIGHT: # If enemy reaches bottom
            self.reached = True
            # Kill self in game.py
