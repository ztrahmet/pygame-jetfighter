"""
game.py

Main menu with buttons for Play, Settings, Quit.
"""

import pygame
from src.button import Button, ButtonGroup
from src.play import Play
from src.settings import Screen
from src.settings import SettingsGUI

class Game:
    """Main game class handling menu and navigation."""

    def __init__(self):
        pygame.init()
        self.running = True
        self.state = "menu"

        self.screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
        pygame.display.set_caption("Jet Fighter")
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont(None, 72)

        # Buttons
        self.create_menu_buttons()

    def create_menu_buttons(self):
        center_x = Screen.WIDTH // 2 - 100
        buttons = [
            Button("Play", center_x, 220, 200, 60, self.start_play),
            Button("Settings", center_x, 320, 200, 60, self.open_settings),
            Button("Quit", center_x, 420, 200, 60, self.quit_game),
        ]
        self.menu_buttons = ButtonGroup(buttons)

    def run(self):
        while self.running:
            self.clock.tick(Screen.FPS)
            if self.state == "menu":
                self.menu_events()
                self.menu_draw()
            elif self.state == "play":
                self.start_play()
            elif self.state == "settings":
                self.open_settings()

        pygame.quit()

    # ---------------- MENU ----------------
    def menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.menu_buttons.handle_event(event)

    def menu_draw(self):
        self.screen.fill((0, 0, 30))
        title = self.title_font.render("Jet Fighter", True, (255, 255, 0))
        self.screen.blit(title, (Screen.WIDTH // 2 - title.get_width() // 2, 100))
        self.menu_buttons.draw(self.screen)
        pygame.display.flip()

    # ---------------- PLAY ----------------
    def start_play(self):
        play = Play()
        result = play.run()
        if result == "gameover":
            self.state = "menu"

    # ---------------- SETTINGS ----------------
    def open_settings(self):
        settings = SettingsGUI(self.screen)
        settings.run()
        self.state = "menu"

    # ---------------- QUIT ----------------
    def quit_game(self):
        self.running = False
