"""
explosion.py

Handle explosion effects in the game.
"""

import pygame
from src.settings import Screen


class Explosion(pygame.sprite.Sprite):
    """Explosion class representing explosion effects."""

    # Image source
    IMAGE_PATH = 'assets/images/explosion.png'

    # Explosion parameters
    DURATION = Screen.FPS // 10  # in frames

    def __init__(self, x: int, y: int):
        """Initialize the explosion."""
        super().__init__()
        self.image = pygame.image.load(self.IMAGE_PATH).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = self.DURATION

        # Play explosion sound
        explosion_sound = pygame.mixer.Sound('assets/sounds/explosion.wav')
        explosion_sound.play()

    def update(self):
        """Update explosion state."""
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
