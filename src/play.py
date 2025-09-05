# -*- coding: utf-8 -*-
"""
play.py

Gameplay loop and logic for Jet Fighter.

This module defines the :class:`Play` class, which manages the player,
enemies, bosses, projectiles, explosions, collisions, HUD, and end-game
sequence. It represents the "play" state of the game.
"""

from __future__ import annotations

import random
from typing import Tuple

import pygame

from src.boss import Boss
from src.database import Database
from src.enemy import Enemy
from src.explosion import Explosion
from src.missile import Missile
from src.player import Player
from src.settings import Screen, Game as GameConfig
from src.gameover import GameOver


class Play:
    """
    Handle the main game loop and gameplay logic.

    Attributes:
        running (bool): Whether the gameplay loop is running.
        db (Database): Database instance for saving scores.
        screen (pygame.Surface): The active game display surface.
        clock (pygame.time.Clock): Controls frame rate.
        all_sprites (pygame.sprite.Group): All active sprites.
        enemies (pygame.sprite.Group): All enemy sprites.
        missiles (pygame.sprite.Group): All missile sprites.
        player (Player): The player-controlled jet fighter.
        score (int): Current score of the player.
        heart_remaining (int): Number of lives left.
        missiles_remaining (int): Number of missiles available.
        font (pygame.font.Font): Font for HUD elements.
        score_image, heart_image, missile_image (pygame.Surface):
            HUD icons for score, heart, and missiles.
    """

    # HUD image paths
    SCORE_IMAGE: str = "assets/images/score.png"
    HEART_IMAGE: str = "assets/images/heart.png"
    MISSILE_IMAGE: str = "assets/images/missile.png"

    # Sound paths
    MILESTONE_SOUND: str = "assets/sounds/milestone.wav"
    GAMEOVER_SOUND: str = "assets/sounds/gameover.wav"
    GAMESTART_SOUND: str = "assets/sounds/gamestart.wav"

    def __init__(self) -> None:
        """Initialize pygame, screen, player, sprite groups, and HUD."""
        pygame.init()

        # Database connection
        self.db: Database = Database()

        # Game loop control
        self.running: bool = True

        # Screen setup
        self.screen: pygame.Surface = pygame.display.set_mode(
            (Screen.WIDTH, Screen.HEIGHT)
        )
        pygame.display.set_caption("Jet Fighter")
        pygame.display.set_icon(pygame.image.load(Player.IMAGE_PATH))
        self.clock: pygame.time.Clock = pygame.time.Clock()

        # Sprite groups
        self.all_sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.enemies: pygame.sprite.Group = pygame.sprite.Group()
        self.missiles: pygame.sprite.Group = pygame.sprite.Group()

        # Player setup
        player_height: int = pygame.image.load(Player.IMAGE_PATH).get_height()
        self.player: Player = Player(
            Screen.WIDTH // 2, Screen.HEIGHT - player_height
        )
        self.all_sprites.add(self.player)

        # Difficulty configuration (enemy spawn rate and max enemies)
        self.enemy_spawn_rate, self.enemy_limit = self.get_difficulty(
            GameConfig.DIFFICULTY
        )

        # Player stats
        self.score: int = 0
        self.heart_remaining: int = GameConfig.HEART
        self.missiles_remaining: int = GameConfig.MISSILES

        # Fonts
        self.font: pygame.font.Font = pygame.font.SysFont(None, 36)

        # HUD images
        self.score_image: pygame.Surface = pygame.image.load(
            self.SCORE_IMAGE
        ).convert_alpha()
        self.heart_image: pygame.Surface = pygame.image.load(
            self.HEART_IMAGE
        ).convert_alpha()
        self.missile_image: pygame.Surface = pygame.image.load(
            self.MISSILE_IMAGE
        ).convert_alpha()

    # ---------------- Difficulty ----------------
    def get_difficulty(self, difficulty: str) -> Tuple[int, int]:
        """
        Return spawn rate (in frames) and enemy limit based on difficulty.

        Args:
            difficulty (str): The current difficulty level.

        Returns:
            tuple[int, int]: (enemy_spawn_rate, enemy_limit).
        """
        match difficulty:
            case "Easy":
                return int(Screen.FPS), 2
            case "Hard":
                return int(Screen.FPS), 5
            case _:
                return int(Screen.FPS), 3

    # ---------------- Run ----------------
    def run(self) -> str:
        """
        Run the gameplay loop until game over.

        Returns:
            str: "gameover" when the game ends.
        """
        # Start sound
        pygame.mixer.Sound(self.GAMESTART_SOUND).play()

        while self.running:
            self.clock.tick(Screen.FPS)
            self.handle_events()
            self.update()
            self.draw()

        return "gameover"

    # ---------------- Events ----------------
    def handle_events(self) -> None:
        """Process player input events (quit, fire missile, etc.)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.missiles_remaining > 0:
                    self.fire_missile()

    def fire_missile(self) -> None:
        """Fire a missile from the player jet."""
        missile = Missile(self.player.rect.centerx, self.player.rect.top)
        self.all_sprites.add(missile)
        self.missiles.add(missile)
        self.missiles_remaining -= 1

    # ---------------- Update ----------------
    def update(self) -> None:
        """Update player, enemies, collisions, and check game conditions."""
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # Game over check
        if self.heart_remaining <= 0 or (
            self.missiles_remaining <= 0 and len(self.missiles) == 0
        ):
            self.end_game()
            return

        # Update non-player sprites
        for sprite in self.all_sprites:
            if sprite != self.player:
                sprite.update()

        # Enemy spawning logic
        if len(self.enemies) < self.enemy_limit:
            if random.randint(1, self.enemy_spawn_rate) == 1:
                self.spawn_enemy()

        # Rare boss spawn
        if random.randint(1, self.enemy_spawn_rate * 10) == 1:
            self.spawn_enemy(is_boss=True)

        # Collision detection
        self.handle_collisions()

    def spawn_enemy(self, is_boss: bool = False) -> None:
        """
        Spawn a new enemy or boss at a random x position.

        Args:
            is_boss (bool): Whether to spawn a boss instead of a normal enemy.
        """
        sprite_cls = Boss if is_boss else Enemy
        enemy_half_width: int = pygame.image.load(
            Enemy.IMAGE_PATH
        ).get_width() // 2

        enemy = sprite_cls(
            random.randint(enemy_half_width, Screen.WIDTH - enemy_half_width),
            -enemy_half_width,
        )
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def handle_collisions(self) -> None:
        """Handle missile-enemy, enemy-player, and enemy-bottom collisions."""
        # Missile-enemy collisions
        hits = pygame.sprite.groupcollide(
            self.missiles, self.enemies, True, True
        )
        for _, enemies_hit in hits.items():
            for enemy in enemies_hit:
                # Missile reward
                self.missiles_remaining += 3 if isinstance(enemy, Boss) else 1
                self.score += 1

                # Explosion
                explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                self.all_sprites.add(explosion)

                # Milestone sound every 10 points
                if self.score % 10 == 0:
                    pygame.mixer.Sound(self.MILESTONE_SOUND).play()

        # Enemy-player collisions
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for hit in hits:
            self.heart_remaining -= 1
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            self.player.blink()
            self.all_sprites.add(explosion)

        # Enemies reaching the bottom
        for enemy in list(self.enemies):
            if enemy.reached:
                self.heart_remaining -= 1
                enemy.kill()

    # ---------------- Draw ----------------
    def draw(self) -> None:
        """Render background, sprites, HUD, and flip the display."""
        background = pygame.transform.scale(
            pygame.image.load(Screen.BACKGROUND_IMAGE),
            (Screen.WIDTH, Screen.HEIGHT),
        )
        self.screen.blit(background, (0, 0))

        # Draw sprites
        self.all_sprites.draw(self.screen)

        # Draw HUD
        self.draw_hud()

        pygame.display.flip()

    def draw_hud(self) -> None:
        """Draw score, hearts, and missiles counters on the HUD."""
        font_count = pygame.font.SysFont(None, 36)

        # Score (top-left)
        score_icon = pygame.transform.scale(self.score_image, (40, 40))
        self.screen.blit(score_icon, (20, 20))
        score_text = font_count.render(str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (70, 25))

        # Hearts (top-right)
        heart_icon = pygame.transform.scale(self.heart_image, (40, 40))
        self.screen.blit(heart_icon, (Screen.WIDTH - 150, 20))
        heart_text = font_count.render(
            f"x{self.heart_remaining}", True, (255, 255, 255)
        )
        self.screen.blit(heart_text, (Screen.WIDTH - 100, 25))

        # Missiles (below hearts)
        missile_icon = pygame.transform.scale(self.missile_image, (40, 40))
        self.screen.blit(missile_icon, (Screen.WIDTH - 150, 80))
        missile_text = font_count.render(
            f"x{self.missiles_remaining}", True, (255, 255, 255)
        )
        self.screen.blit(missile_text, (Screen.WIDTH - 100, 85))

    # ---------------- End game ----------------
    def end_game(self) -> None:
        """Stop gameplay, save score, play sound, and show Game Over screen."""
        self.running = False
        self.db.save_score(self.score, GameConfig.DIFFICULTY)

        # Game over sound
        pygame.mixer.Sound(self.GAMEOVER_SOUND).play()

        # Capture screen
        background_snapshot: pygame.Surface = self.screen.copy()

        # Show Game Over overlay
        game_over = GameOver(self.score, background_snapshot)
        game_over.run()
