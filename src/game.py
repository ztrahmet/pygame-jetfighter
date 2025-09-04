"""
game.py

Main game logic and loop.
"""

import pygame
import random
from src.database import Database
from src.enemy import Enemy
from src.explosion import Explosion
from src.missile import Missile
from src.player import Player
from src.settings import Screen, Game as Game_CONFIG


class Game:
    """Main game class to handle game logic and loop."""

    def __init__(self):
        """Initialize the game."""
        pygame.init()

        self.db = Database()

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

        # Player
        player_height = pygame.image.load(Player.IMAGE_PATH).get_width()
        self.player = Player(Screen.WIDTH // 2, Screen.HEIGHT - player_height)
        self.all_sprites.add(self.player)

        # Difficulty
        match Game_CONFIG.DIFFICULTY:
            case 'Easy':
                self.enemy_spawn_rate = Screen.FPS * 2  # Spawn every 2 seconds
            case 'Hard':
                self.enemy_spawn_rate = Screen.FPS // 2  # Spawn every half second
            case _:
                self.enemy_spawn_rate = Screen.FPS  # Spawn every second

        # Game stats
        self.score = 0
        self.heart_remaining = Game_CONFIG.HEART
        self.missiles_remaining = Game_CONFIG.MISSILES

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
                if event.key == pygame.K_SPACE and self.missiles_remaining > 0:
                    missile = Missile(self.player.rect.centerx, self.player.rect.top)
                    self.all_sprites.add(missile)
                    self.missiles.add(missile)
                    self.missiles_remaining -= 1

    def update(self):
        """Update all game elements."""
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # Check for game over
        if self.heart_remaining <= 0 or (self.missiles_remaining <= 0 and len(self.missiles) == 0):
            self.running = False
            self.db.save_score(self.score)
            print(f"Game Over! Your score: {self.score}")
            print("Top Scores:", self.db.get_high_scores(5))

        # Update all other sprites (except player)
        for sprite in self.all_sprites:
            if sprite != self.player:
                sprite.update()

        # Spawn enemies randomly
        if random.randint(1, self.enemy_spawn_rate) == 1:  # Random spawn based on difficulty
            # Get enemy image width for boundaries
            enemy_half_width = pygame.image.load(Enemy.IMAGE_PATH).get_width() // 2

            enemy = Enemy(
                random.randint(enemy_half_width, Screen.WIDTH - enemy_half_width),
                -1 * enemy_half_width # Start just above the screen
            )
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        # Missile-enemy collisions (enemy explodes)
        hits = pygame.sprite.groupcollide(self.missiles, self.enemies, True, True)
        for _, enemies_hit in hits.items():
            for enemy in enemies_hit:
                self.score += 1
                self.missiles_remaining += 1

                # Create explosion on the hit position
                explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                self.all_sprites.add(explosion)

        # Enemy-player collisions (both explode)
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for hit in hits:
            self.heart_remaining -= 1
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            self.player.blink() # Start player blink effect
            self.all_sprites.add(explosion)

        # Enemy reachs bottom
        for enemy in list(self.enemies):
            if enemy.reached == True:
                self.heart_remaining -= 1
                enemy.kill()

    def draw(self):
        """Draw all game elements."""

        # Background Image (stretch to fit screen)
        background = pygame.transform.scale(
            pygame.image.load(Screen.BACKGROUND_IMAGE),
            (Screen.WIDTH, Screen.HEIGHT)
        )
        self.screen.blit(background, (0, 0))
        self.all_sprites.draw(self.screen)

        pygame.display.flip()  # Update the full display surface to the screen
