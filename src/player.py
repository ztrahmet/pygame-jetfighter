"""
player.py

Handle player character and related actions.
"""

import pygame
from src.settings import Player as Player_CONFIG, Screen


class Player(pygame.sprite.Sprite):
    """Player class representing the jet fighter."""

    # Image source
    IMAGE_PATH = 'assets/images/player.png'

    # Blinking effect parameters
    BLINK_DURATION = Screen.FPS // 10 # in frames
    BLINK_COUNT = 5

    # Player configuration
    SPEED = Player_CONFIG.SPEED

    def __init__(self, x: int, y: int):
        """Initialize the player."""
        super().__init__()
        self.image = pygame.image.load(self.IMAGE_PATH).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.blink_timer = 0
        self.blink_count = 0
    
    def update(self, keys):
        """Update player position based on key presses."""
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < Screen.WIDTH:
            self.rect.x += self.SPEED
        
        # Handle blinking effect
        if self.blink_count > 0:
            self.blink_timer -= 1
            if self.blink_timer <= 0:
                # Toggle alpha between 128 and 255
                current_alpha = self.image.get_alpha()
                self.image.set_alpha(255 if current_alpha == 128 else 128)
                self.blink_count -= 1
                self.blink_timer = self.BLINK_DURATION
        else:
            self.image.set_alpha(255)
    
    def blink(self):
        """Start the blink effect (for invincibility frames)."""
        self.blink_count = self.BLINK_COUNT
        self.blink_timer = self.BLINK_DURATION
        self.image.set_alpha(128)
