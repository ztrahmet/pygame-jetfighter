"""
game.py

Main game logic and loop.
"""

import pygame
from src.database import Database
from src.enemy import Enemy
from src.explosion import Explosion
from src.missile import Missile
from src.player import Player
from src.settings import Screen


class Game:
    """Main game class to handle game logic and loop."""

    def __init__(self):
        """Initialize the game."""
        pygame.init()

        # Game state 
        self.running = True
        
        # Screen setup
        self.screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
        pygame.display.set_caption("Jet Fighter")
        pygame.display.set_icon(pygame.image.load("assets/images/player.png"))
        
        self.clock = pygame.time.Clock()

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        # Player
        self.player = Player(Screen.WIDTH // 2, Screen.HEIGHT - 64)
        self.all_sprites.add(self.player)

        # Score
        self.score = 0

        # Font
        self.font = pygame.font.SysFont(None, 36)

    def run(self):
        """Main game loop."""
        while self.running:
            self.clock.tick(Screen.FPS)
            self.events()
            self.update()
            self.draw()
        pygame.quit()

    def events(self):
        """Handle all events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    missile = Missile(self.player.rect.centerx, self.player.rect.top)
                    self.all_sprites.add(missile)
                    self.missiles.add(missile)
    
    def update(self):
        """Update all game elements."""
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # Update all other sprites (except player)
        for sprite in self.all_sprites:
            if sprite != self.player:
                sprite.update()

        # Spawn enemies randomly

        # Bullet-enemy collisions

        # Enemy-player collisions
    
    def draw(self):
        """Draw all game elements."""
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)

        pygame.display.flip() # Update the full display surface to the screen
