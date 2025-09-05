# -*- coding: utf-8 -*-
"""
gameover.py

Game Over screen for Jet Fighter.

This module defines the :class:`GameOver` class, which displays the final
score, top high scores, and a button to return to the main menu after a game
session ends.
"""

from __future__ import annotations

import pygame

from src.button import Button, ButtonGroup
from src.database import Database
from src.settings import Screen


class GameOver:
    """
    Display the Game Over screen and leaderboard.

    Attributes:
        score (int): The player's final score.
        background (pygame.Surface): A snapshot of the screen before game over.
        screen (pygame.Surface): The active game surface.
        font_large (pygame.font.Font): Font for large texts.
        font_small (pygame.font.Font): Font for smaller texts.
        buttons (ButtonGroup): Group of interactive buttons.
        running (bool): Whether the game over loop is active.
        db (Database): Database instance for retrieving high scores.
    """

    def __init__(self, score: int, background: pygame.Surface) -> None:
        """Initialize Game Over screen with score, fonts, and UI elements."""
        self.score: int = score
        self.background: pygame.Surface = background
        self.screen: pygame.Surface = pygame.display.set_mode(
            (Screen.WIDTH, Screen.HEIGHT)
        )

        # Fonts
        self.font_large: pygame.font.Font = pygame.font.SysFont(None, 72)
        self.font_small: pygame.font.Font = pygame.font.SysFont(None, 36)

        # Database connection
        self.db: Database = Database()

        # Buttons
        self.create_buttons()

        # Control flag
        self.running: bool = True
    
    def create_buttons(self) -> None:
        """Initialize the game over screen buttons and group them together."""
        center_x: int = Screen.WIDTH // 2 - 100
        buttons = [
            Button("Main Menu", center_x, 500, 200, 60, self.close),
        ]
        self.buttons: ButtonGroup = ButtonGroup(buttons)

    # ---------------- Main loop ----------------
    def run(self) -> None:
        """Run the Game Over loop until the player chooses to exit."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.buttons.handle_event(event)

            self.draw()
            pygame.display.flip()

    # ---------------- Actions ----------------
    def close(self) -> None:
        """Close the Game Over screen and return control to the main menu."""
        self.running = False
    
    # ---------------- Records ----------------
    def draw_records(self) -> None:
        """
        Draw the top high scores table centered on the screen.
        Uses font_large for headers and font_small for table rows.
        """
        # Fetch top 5 scores
        high_scores = self.db.get_high_scores(5)

        # Table layout
        header_y = 220
        row_height = 40
        col_widths = [100, 150, 200]  # Score, Difficulty, Date
        table_width = sum(col_widths) + 40  # extra padding
        start_x = (Screen.WIDTH - table_width) // 2

        # Column positions
        col_score = start_x
        col_difficulty = col_score + col_widths[0] + 20
        col_date = col_difficulty + col_widths[1] + 20

        # Draw headers
        header_score = self.font_small.render("Score", True, (255, 255, 0))
        header_difficulty = self.font_small.render("Difficulty", True, (255, 255, 0))
        header_date = self.font_small.render("Date", True, (255, 255, 0))

        self.screen.blit(header_score, (col_score, header_y))
        self.screen.blit(header_difficulty, (col_difficulty, header_y))
        self.screen.blit(header_date, (col_date, header_y))

        # Draw line under headers
        pygame.draw.line(
            self.screen, (255, 255, 255),
            (start_x, header_y + 40),
            (start_x + table_width, header_y + 40),
            2
        )

        # Draw rows
        row_y = header_y + 50
        for score, difficulty, created_at in high_scores:
            score_text = self.font_small.render(str(score), True, (255, 255, 255))
            difficulty_text = self.font_small.render(str(difficulty), True, (255, 255, 255))
            date_text = self.font_small.render(str(created_at), True, (255, 255, 255))

            self.screen.blit(score_text, (col_score, row_y))
            self.screen.blit(difficulty_text, (col_difficulty, row_y))
            self.screen.blit(date_text, (col_date, row_y))

            row_y += row_height

    # ---------------- Drawing ----------------
    def draw(self) -> None:
        """Render the Game Over screen with final score and high scores."""
        # Background snapshot
        self.screen.blit(self.background, (0, 0))
        overlay = pygame.Surface((Screen.WIDTH, Screen.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent dark overlay
        self.screen.blit(overlay, (0, 0))

        # "Game Over" title
        title = self.font_large.render("Game Over", True, (255, 0, 0))
        self.screen.blit(
            title, (Screen.WIDTH // 2 - title.get_width() // 2, 100)
        )

        # Final score
        score_text = self.font_small.render(
            f"Your Score: {self.score}", True, (255, 255, 255)
        )
        self.screen.blit(
            score_text, (Screen.WIDTH // 2 - score_text.get_width() // 2, 150)
        )

        # Draw top scores
        self.draw_records()

        # Buttons
        self.buttons.draw(self.screen)
