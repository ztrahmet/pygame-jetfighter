"""
boss.py

Special Boss enemy that inherits from Enemy.
Spawns rarely and rewards multiple missiles on defeat.
"""

import pygame
from src.enemy import Enemy


class Boss(Enemy):
    """Boss enemy with higher health and bigger sprite."""

    # Image source
    IMAGE_PATH = 'assets/images/boss.png'

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.image = pygame.image.load(self.IMAGE_PATH).convert_alpha()
