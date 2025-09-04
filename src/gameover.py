"""
gameover.py

Game Over screen with top 5 high scores in a table format and Main Menu button.
"""

import pygame
from src.settings import Screen
from src.database import Database


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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()


class GameOver:
    """Displays Game Over screen with top 5 scores in table format."""

    def __init__(self, score: int, background_surface: pygame.Surface):
        pygame.init()
        self.running = True
        self.score = score

        # Capture game screen
        self.background_surface = background_surface.copy()

        # Database for scores
        self.db = Database()
        # List of tuples: (score, date_string)
        self.top_scores = self.db.get_high_scores(5)  

        # Setup screen
        self.screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
        pygame.display.set_caption("Game Over")

        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont(None, 72)
        self.font_header = pygame.font.SysFont(None, 48)
        self.font_cell = pygame.font.SysFont(None, 36)

        # Button
        btn_width, btn_height = 250, 60
        self.menu_button = Button(
            text="Main Menu",
            x=Screen.WIDTH // 2 - btn_width // 2,
            y=500,
            width=btn_width,
            height=btn_height,
            callback=self.return_to_menu,
        )

        # Transparent overlay (10%)
        self.overlay = pygame.Surface((Screen.WIDTH, Screen.HEIGHT))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(25)  # ~10% opacity

    def return_to_menu(self):
        """Stop the Game Over screen and return to menu."""
        self.running = False

    def run(self):
        """Show Game Over screen until player clicks Main Menu."""
        while self.running:
            self.clock.tick(Screen.FPS)
            self.handle_events()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.menu_button.handle_event(event)

    def draw(self):
        # Draw last game frame as background
        self.screen.blit(self.background_surface, (0, 0))

        # Draw semi-transparent overlay (10% opacity)
        self.screen.blit(self.overlay, (0, 0))

        # Draw "GAME OVER" title
        title = self.font_title.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(title, (Screen.WIDTH // 2 - title.get_width() // 2, 50))

        # Table headers
        header_y = 180
        col_widths = [100, 150, 200]  # Rank, Score, Date
        table_width = sum(col_widths) + 40  # spacing between columns
        start_x = Screen.WIDTH // 2 - table_width // 2

        col_rank = start_x
        col_score = col_rank + col_widths[0] + 20
        col_date = col_score + col_widths[1] + 20

        header_rank = self.font_header.render("Rank", True, (255, 255, 0))
        header_score = self.font_header.render("Score", True, (255, 255, 0))
        header_date = self.font_header.render("Date", True, (255, 255, 0))

        self.screen.blit(header_rank, (col_rank, header_y))
        self.screen.blit(header_score, (col_score, header_y))
        self.screen.blit(header_date, (col_date, header_y))

        # Draw horizontal line under header
        pygame.draw.line(self.screen, (255, 255, 255), (start_x, header_y + 50), (start_x + table_width, header_y + 50), 2)

        # Draw table rows
        row_y = header_y + 70
        rank = 1
        for entry in self.top_scores:
            rank_text = self.font_cell.render(str(rank), True, (255, 255, 255))
            score_text = self.font_cell.render(str(entry[0]), True, (255, 255, 255))
            date_text = self.font_cell.render(str(entry[1]), True, (255, 255, 255))

            self.screen.blit(rank_text, (col_rank, row_y))
            self.screen.blit(score_text, (col_score, row_y))
            self.screen.blit(date_text, (col_date, row_y))

            row_y += 50
            rank += 1

        # Draw Main Menu button
        self.menu_button.draw(self.screen)

        # Update display
        pygame.display.flip()
