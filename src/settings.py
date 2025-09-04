"""
settings.py

Global configuration constants for the game, including screen, player, and enemy settings.
"""

import pygame
from src.button import Button, ButtonGroup


class Screen:
    """Screen configuration constants."""
    WIDTH = 800
    HEIGHT = 600
    FPS = 60
    BACKGROUND_IMAGE = 'assets/images/background.png'


class Game:
    """Game configuration constants."""
    DIFFICULTY = 'Normal'
    HEART = 3
    MISSILES = 5


class Player:
    """Player configuration constants."""
    SPEED = 6
    MISSILE_SPEED = 7


class Enemy:
    """Enemy configuration constants."""
    SPEED = 3

class SettingsGUI:
    """Settings GUI with buttons."""

    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont(None, 64)
        self.create_buttons()

    def create_buttons(self):
        center_x = Screen.WIDTH // 2 - 100
        y_start = 200
        spacing = 80

        buttons = []

        # Difficulty buttons
        for i, diff in enumerate(["Easy", "Normal", "Hard"]):
            def make_callback(d=diff):
                return lambda: self.set_difficulty(d)
            btn = Button(diff, center_x, y_start + i*spacing, 200, 60, make_callback())
            buttons.append(btn)

        # Back button
        back_btn = Button("Back", center_x, y_start + len(["Easy","Normal","Hard"])*spacing, 200, 60, self.exit)
        buttons.append(back_btn)

        self.button_group = ButtonGroup(buttons)

    def set_difficulty(self, difficulty):
        Game.DIFFICULTY = difficulty

    def exit(self):
        self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.button_group.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.exit()

    def draw(self):
        self.screen.fill((20, 20, 40))
        title = self.title_font.render("Settings", True, (0, 255, 255))
        self.screen.blit(title, (Screen.WIDTH // 2 - title.get_width() // 2, 100))

        info_font = pygame.font.SysFont(None, 36)
        info_text = info_font.render(f"Current Difficulty: {Game.DIFFICULTY}", True, (255,255,255))
        self.screen.blit(info_text, (Screen.WIDTH//2 - info_text.get_width()//2, 500))

        self.button_group.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(Screen.FPS)
            self.handle_events()
            self.draw()
