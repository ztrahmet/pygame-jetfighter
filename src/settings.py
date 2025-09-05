# -*- coding: utf-8 -*-
"""
settings.py

Game configuration and settings menu for Jet Fighter.

This module contains:
- Global screen and gameplay constants (sizes, FPS, assets).
- The SettingsGUI class, which allows the player to configure difficulty
  interactively via a button menu.
"""

from __future__ import annotations

import pygame

from src.button import Button, ButtonGroup


class Screen:
    """Screen configuration constants."""

    WIDTH: int = 800
    HEIGHT: int = 600
    FPS: int = 60
    BACKGROUND_IMAGE: str = "assets/images/background.png"


class Game:
    """Gameplay configuration constants."""

    DIFFICULTY: str = "Normal"  # Default difficulty
    HEART: int = 3              # Initial number of lives
    MISSILES: int = 10          # Initial missile count


class SettingsGUI:
    """
    In-game settings menu for configuring difficulty.

    Attributes:
        screen (pygame.Surface): The active game surface.
        font (pygame.font.Font): Font for rendering text.
        buttons (ButtonGroup): Group of interactive buttons.
        running (bool): Whether the settings menu loop is active.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize the settings menu with difficulty buttons."""
        self.screen: pygame.Surface = screen
        self.font: pygame.font.Font = pygame.font.SysFont(None, 48)
        self.small_font: pygame.font.Font = pygame.font.SysFont(None, 32)
        self.running: bool = True

        # Create interactive buttons for the settings menu
        self.create_buttons()
    
    def create_buttons(self) -> None:
        """Initialize the settings menu buttons and group them together."""
        center_x: int = Screen.WIDTH // 2 - 100
        buttons = [
            Button("Easy", center_x, 180, 200, 60, lambda: self.set_difficulty("Easy")),
            Button("Normal", center_x, 250, 200, 60, lambda: self.set_difficulty("Normal")),
            Button("Hard", center_x, 320, 200, 60, lambda: self.set_difficulty("Hard")),
            Button("Back", center_x, 400, 200, 60, self.close),
        ]
        self.buttons: ButtonGroup = ButtonGroup(buttons)

    # ---------------- Menu loop ----------------
    def run(self) -> None:
        """Run the settings menu loop until closed."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.buttons.handle_event(event)

            self.draw()
            pygame.display.flip()

    # ---------------- Button actions ----------------
    def set_difficulty(self, difficulty: str) -> None:
        """
        Set the global game difficulty and close the menu.

        Args:
            difficulty (str): The difficulty level to set.
        """
        Game.DIFFICULTY = difficulty
        self.running = False

    def close(self) -> None:
        """Close the settings menu without changes."""
        self.running = False

    # ---------------- Drawing ----------------
    def draw(self) -> None:
        """Render the settings menu UI on the screen."""
        self.screen.fill((0, 0, 30))

        # Title
        title: pygame.Surface = self.font.render("Settings", True, (255, 255, 0))
        self.screen.blit(title, (Screen.WIDTH // 2 - title.get_width() // 2, 100))

        # Current difficulty info
        difficulty_text: pygame.Surface = self.small_font.render(
            f"Current Difficulty: {Game.DIFFICULTY}", True, (200, 200, 200)
        )
        self.screen.blit(difficulty_text,
                         (Screen.WIDTH // 2 - difficulty_text.get_width() // 2, 150))

        # Buttons
        self.buttons.draw(self.screen)
