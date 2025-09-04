"""
play.py

Main gameplay logic and loop for Jet Fighter.
"""

import pygame
import random
from src.boss import Boss
from src.database import Database
from src.enemy import Enemy
from src.explosion import Explosion
from src.missile import Missile
from src.player import Player
from src.settings import Screen, Game as Game_CONFIG
from src.gameover import GameOver


class Play:
    """Class that handles the main game loop."""
    
    # HUD Image Source
    SCORE_IMAGE = 'assets/images/score.png'
    HEART_IMAGE = 'assets/images/heart.png'
    MISSILE_IMAGE = 'assets/images/missile.png'

    # Sound Source
    MILESTONE_SOUND = 'assets/sounds/milestone.wav'
    GAMEOVER_SOUND = 'assets/sounds/gameover.wav'
    GAMESTART_SOUND = 'assets/sounds/gamestart.wav'

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
        
        self.score_image = pygame.image.load(self.SCORE_IMAGE).convert_alpha()
        self.heart_image = pygame.image.load(self.HEART_IMAGE).convert_alpha()
        self.missile_image = pygame.image.load(self.MISSILE_IMAGE).convert_alpha()

    def get_spawn_rate(self, difficulty: str) -> int:
        """Return spawn rate (in frames) based on difficulty setting."""
        match difficulty:
            case 'Easy':
                return int(Screen.FPS * 1.7)  # 1 enemy every 1.7 seconds
            case 'Hard':
                return int(Screen.FPS / 1.3)  # 1.3 enemies per second
            case _:
                return int(Screen.FPS * 1.3)  # Default: 1 enemy per 1.3 second

    def run(self):
        """Main gameplay loop."""
        # Play game start sound
        pygame.mixer.Sound(self.GAMESTART_SOUND).play()

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
        
        # Rare boss spawn
        if random.randint(1, self.enemy_spawn_rate * 10) == 1:
            self.spawn_enemy(is_boss=True)

        # Handle collisions
        self.handle_collisions()

    def spawn_enemy(self, is_boss: bool = False):
        """Spawn a new enemy at a random x position."""
        if is_boss:
            sprite_cls = Boss
        else:
            sprite_cls = Enemy

        enemy_half_width = pygame.image.load(Enemy.IMAGE_PATH).get_width() // 2
        enemy = sprite_cls(
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
                if isinstance(enemy, Boss):
                    self.missiles_remaining += 3
                else:
                    self.missiles_remaining += 1
                self.score += 1
                explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                self.all_sprites.add(explosion)

                # Milestone sound on each 10 scores
                if self.score % 10 == 0:
                    pygame.mixer.Sound(self.MILESTONE_SOUND).play()


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

        # Draw all sprites
        self.all_sprites.draw(self.screen)

        # Draw HUD on top
        self.draw_hud()

        pygame.display.flip()
    
    def draw_hud(self):
        """Draw hearts, missiles, and score with count next to icons."""

        # Fonts
        font_count = pygame.font.SysFont(None, 36)

        # Score at top-left
        score_icon = pygame.transform.scale(self.score_image, (40, 40))
        self.screen.blit(score_icon, (20, 20))
        score_text = font_count.render(str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (70, 25))

        # Hearts at top-right
        heart_icon = pygame.transform.scale(self.heart_image, (40, 40))
        self.screen.blit(heart_icon, (Screen.WIDTH - 150, 20))
        heart_text = font_count.render(f"x{self.heart_remaining}", True, (255, 255, 255))
        self.screen.blit(heart_text, (Screen.WIDTH - 100, 25))

        # Missiles next to hearts
        missile_icon = pygame.transform.scale(self.missile_image, (40, 40))
        self.screen.blit(missile_icon, (Screen.WIDTH - 150, 80))
        missile_text = font_count.render(f"x{self.missiles_remaining}", True, (255, 255, 255))
        self.screen.blit(missile_text, (Screen.WIDTH - 100, 85))

    # ---------------- End game ----------------
    def end_game(self):
        """Handle end of game: save score and show Game Over screen."""
        self.running = False
        self.db.save_score(self.score, Game_CONFIG.DIFFICULTY)

        # Play game over sound
        pygame.mixer.Sound(self.GAMEOVER_SOUND).play()

        # Capture the current screen
        background_snapshot = self.screen.copy()

        # Show Game Over screen with transparent overlay
        game_over = GameOver(self.score, background_snapshot)
        game_over.run()
