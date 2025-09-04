"""
game.py

Main game menu with clickable buttons for navigation.
"""

import pygame
from src.play import Play
from src.settings import Screen


class Button:
    """Reusable button widget."""

    def __init__(self, text, x, y, width, height, callback,
                 font_size=40,
                 color_idle=(50, 50, 50),
                 color_hover=(100, 100, 100),
                 text_color=(255, 255, 255)):

        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.color_idle = color_idle
        self.color_hover = color_hover
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, font_size)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.color_hover if self.rect.collidepoint(mouse_pos) else self.color_idle
        pygame.draw.rect(surface, color, self.rect, border_radius=10)

        text_surf = self.font.render(self.text, True, self.text_color)
        surface.blit(
            text_surf,
            (self.rect.centerx - text_surf.get_width() // 2,
             self.rect.centery - text_surf.get_height() // 2)
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if self.rect.collidepoint(event.pos):
                self.callback()


class Game:
    """Main game class to handle menu and navigation."""

    def __init__(self) -> None:
        pygame.init()
        self.running = True
        self.state = "menu"  # "menu", "play", "settings"

        # Setup screen
        self.screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
        pygame.display.set_caption("Jet Fighter")
        self.clock = pygame.time.Clock()

        # Fonts
        self.title_font = pygame.font.SysFont(None, 72)

        # Buttons
        self.buttons = []
        self.create_menu_buttons()

    def create_menu_buttons(self):
        """Create menu buttons with actions."""
        center_x = Screen.WIDTH // 2 - 100
        self.buttons = [
            Button("Play", center_x, 220, 200, 60, self.start_play),
            Button("Settings", center_x, 320, 200, 60, self.open_settings),
            Button("Quit", center_x, 420, 200, 60, self.quit_game),
        ]

    def run(self):
        """Main loop for menu and state handling."""
        while self.running:
            self.clock.tick(Screen.FPS)
            if self.state == "menu":
                self.menu_events()
                self.menu_draw()
            elif self.state == "play":
                self.start_play()
            elif self.state == "settings":
                self.settings_events()
                self.settings_draw()

        pygame.quit()

    # ---------------- MENU ----------------
    def menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            for btn in self.buttons:
                btn.handle_event(event)

    def menu_draw(self):
        self.screen.fill((0, 0, 30))
        title = self.title_font.render("Jet Fighter", True, (255, 255, 0))
        self.screen.blit(title, (Screen.WIDTH // 2 - title.get_width() // 2, 100))

        for btn in self.buttons:
            btn.draw(self.screen)

        pygame.display.flip()

    # ---------------- PLAY ----------------
    def start_play(self):
        """Start the actual game loop."""
        play = Play()
        result = play.run()

        if result == "gameover":
            # After game over, return to menu
            self.state = "menu"

    # ---------------- SETTINGS ----------------
    def open_settings(self):
        self.state = "settings"

    def settings_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "menu"

    def settings_draw(self):
        self.screen.fill((20, 20, 20))
        settings_title = self.title_font.render("Settings (ESC to return)", True, (0, 255, 255))
        self.screen.blit(settings_title, (Screen.WIDTH // 2 - settings_title.get_width() // 2, 100))

        difficulty_text = self.title_font.render("Difficulty: Normal", True, (255, 255, 255))
        self.screen.blit(difficulty_text, (Screen.WIDTH // 2 - difficulty_text.get_width() // 2, 250))

        pygame.display.flip()

    # ---------------- QUIT ----------------
    def quit_game(self):
        self.running = False
