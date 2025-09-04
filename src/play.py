"""
play.py

Main gameplay logic and loop for Jet Fighter.
"""

import pygame
import random
from src.database import Database
from src.enemy import Enemy
from src.explosion import Explosion
from src.missile import Missile
from src.player import Player
from src.settings import Screen, Game as Game_CONFIG
from src.gameover import GameOver


class Play:
    """Class that handles the main game loop."""

    def __init__(self):
        pygame.init()

        # Database for scores
        self.db = Database()

        # Game state
        self.running = True

        # Screen setup
        self.screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
        pygame.display.set_caption("Jet Fighter")
        pygame.display.set_icon(pygame.image.load(Player.IMAGE_PATH))

        self.clock = pygame.time.Clock()

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()

        # Player setup
        player_height = pygame.image.load(Player.IMAGE_PATH).get_height()
        self.player = Player(Screen.WIDTH // 2, Screen.HEIGHT - player_height)
        self.all_sprites.add(self.player)

        # Difficulty spawn rate
        self.enemy_spawn_rate = self.get_spawn_rate(Game_CONFIG.DIFFICULTY)

        # Stats
        self.score = 0
        self.heart_remaining = Game_CONFIG.HEART
        self.missiles_remaining = Game_CONFIG.MISSILES

        # Fonts
        self.font = pygame.font.SysFont(None, 36)

    def get_spawn_rate(self, difficulty: str) -> int:
        """Return spawn rate (in frames) based on difficulty setting."""
        match difficulty:
            case 'Easy':
                return Screen.FPS * 2     # 1 enemy every 2 seconds
            case 'Hard':
                return Screen.FPS // 2    # 2 enemies per second
            case _:
                return Screen.FPS         # Default: 1 enemy per second

    def run(self):
        """Main gameplay loop."""
        while self.running:
            self.clock.tick(Screen.FPS)
            self.handle_events()
            self.update()
            self.draw()

        # After game ends, return state
        return "gameover"

    # ---------------- Events ----------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.missiles_remaining > 0:
                    self.fire_missile()

    def fire_missile(self):
        """Fire a missile from the player’s jet."""
        missile = Missile(self.player.rect.centerx, self.player.rect.top)
        self.all_sprites.add(missile)
        self.missiles.add(missile)
        self.missiles_remaining -= 1

    # ---------------- Update ----------------
    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # Game over conditions
        if self.heart_remaining <= 0 or (
            self.missiles_remaining <= 0 and len(self.missiles) == 0
        ):
            self.end_game()
            return

        # Update all other sprites
        for sprite in self.all_sprites:
            if sprite != self.player:
                sprite.update()

        # Spawn enemies randomly
        if random.randint(1, self.enemy_spawn_rate) == 1:
            self.spawn_enemy()

        # Handle collisions
        self.handle_collisions()

    def spawn_enemy(self):
        """Spawn a new enemy at a random x position."""
        enemy_half_width = pygame.image.load(Enemy.IMAGE_PATH).get_width() // 2
        enemy = Enemy(
            random.randint(enemy_half_width, Screen.WIDTH - enemy_half_width),
            -enemy_half_width,
        )
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def handle_collisions(self):
        """Check and handle all collisions."""

        # Missile-enemy
        hits = pygame.sprite.groupcollide(self.missiles, self.enemies, True, True)
        for _, enemies_hit in hits.items():
            for enemy in enemies_hit:
                self.score += 1
                self.missiles_remaining += 1
                explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                self.all_sprites.add(explosion)

        # Enemy-player
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for hit in hits:
            self.heart_remaining -= 1
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            self.player.blink()
            self.all_sprites.add(explosion)

        # Enemy reaches bottom
        for enemy in list(self.enemies):
            if enemy.reached:
                self.heart_remaining -= 1
                enemy.kill()

    # ---------------- Draw ----------------
    def draw(self):
        # Background
        background = pygame.transform.scale(
            pygame.image.load(Screen.BACKGROUND_IMAGE),
            (Screen.WIDTH, Screen.HEIGHT),
        )
        self.screen.blit(background, (0, 0))

        # Sprites
        self.all_sprites.draw(self.screen)

        # HUD
        hud_text = self.font.render(
            f"Score: {self.score}  Hearts: {self.heart_remaining}  Missiles: {self.missiles_remaining}",
            True,
            (255, 255, 255),
        )
        self.screen.blit(hud_text, (10, 10))

        pygame.display.flip()

    # ---------------- End game ----------------
    def end_game(self):
        """Handle end of game: save score and show Game Over screen."""
        self.running = False
        self.db.save_score(self.score)

        # Capture the current screen
        background_snapshot = self.screen.copy()

        # Show Game Over screen with transparent overlay
        game_over = GameOver(self.score, background_snapshot)
        game_over.run()
