# -*- coding: utf-8 -*-
"""
game.py

Main menu and high-level game navigation for Jet Fighter.

This module defines the :class:`Game` class, which manages the main menu,
state transitions (menu, play, settings), and quitting the application.

It uses reusable Button and ButtonGroup classes for menu navigation.
"""

from __future__ import annotations

import pygame

from src.button import Button, ButtonGroup
from src.play import Play
from src.settings import Screen, SettingsGUI


class Game:
    """
    Main game class handling the menu, navigation, and high-level states.

    Attributes:
        running (bool): Whether the game loop should continue.
        state (str): Current state of the game ("menu", "play", "settings").
        screen (pygame.Surface): The main game screen.
        clock (pygame.time.Clock): The frame rate controller.
        title_font (pygame.font.Font): Font used for the main title.
        menu_buttons (ButtonGroup): Buttons displayed on the main menu.
    """

    # Background music (disabled by default)
    MUSIC_SOUND: str = "assets/sounds/music.wav"

    def __init__(self) -> None:
        """Initialize pygame, screen, clock, fonts, and menu buttons."""
        pygame.init()
        self.running: bool = True
        self.state: str = "menu"

        # Setup display screen
        self.screen: pygame.Surface = pygame.display.set_mode(
            (Screen.WIDTH, Screen.HEIGHT)
        )
        pygame.display.set_caption("Jet Fighter")
        self.clock: pygame.time.Clock = pygame.time.Clock()

        # Background music setup (commented out for now)
        # pygame.mixer.music.load(self.MUSIC_SOUND)
        # pygame.mixer.music.set_volume(0.2)
        # pygame.mixer.music.play(-1)  # Loop indefinitely

        self.title_font: pygame.font.Font = pygame.font.SysFont(None, 72)

        # Create interactive buttons for the main menu
        self.create_buttons()

    def create_buttons(self) -> None:
        """Initialize the main menu buttons and group them together."""
        center_x: int = Screen.WIDTH // 2 - 100
        buttons: list[Button] = [
            Button("Play", center_x, 180, 200, 60, self.start_play),
            Button("Settings", center_x, 250, 200, 60, self.open_settings),
            Button("Quit", center_x, 320, 200, 60, self.quit_game),
        ]
        self.menu_buttons: ButtonGroup = ButtonGroup(buttons)

    def run(self) -> None:
        """
        Main loop of the game.

        Continuously checks the current state (menu, play, settings) and
        executes the appropriate handlers until the game is stopped.
        """
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
    def menu_events(self) -> None:
        """Process events in the main menu (quit, button clicks, navigation)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.menu_buttons.handle_event(event)

    def menu_draw(self) -> None:
        """Draw the main menu background, title, buttons, and footer."""
        # Background color
        self.screen.fill((0, 0, 30))

        # Title
        title: pygame.Surface = self.title_font.render(
            "Jet Fighter", True, (255, 255, 0)
        )
        self.screen.blit(
            title, (Screen.WIDTH // 2 - title.get_width() // 2, 100)
        )

        # Buttons
        self.menu_buttons.draw(self.screen)

        # Footer text
        footer_font: pygame.font.Font = pygame.font.SysFont(None, 20)
        footer_text: pygame.Surface = footer_font.render(
            "CS50x 2025: Final Project", True, (200, 200, 200)
        )
        self.screen.blit(footer_text, (10, Screen.HEIGHT - 25))

        pygame.display.flip()

    # ---------------- PLAY ----------------
    def start_play(self) -> None:
        """
        Start the gameplay loop.

        When the Play loop ends, return to the main menu state.
        """
        play = Play()
        result: str = play.run()
        if result == "gameover":
            self.state = "menu"

    # ---------------- SETTINGS ----------------
    def open_settings(self) -> None:
        """
        Open the settings GUI.

        When settings are closed, return to the main menu state.
        """
        settings = SettingsGUI(self.screen)
        settings.run()
        self.state = "menu"

    # ---------------- QUIT ----------------
    def quit_game(self) -> None:
        """Exit the game loop and terminate the program."""
        self.running = False
