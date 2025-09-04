"""
gameover.py

Game Over screen with top 5 scores in table format and Main Menu button.
"""

import pygame
from src.settings import Screen
from src.database import Database
from src.button import Button, ButtonGroup

class GameOver:
    """Game Over screen."""

    def __init__(self, score, background_surface):
        pygame.init()
        self.running = True
        self.score = score
        self.background_surface = background_surface.copy()

        # Database
        self.db = Database()
        self.top_scores = self.db.get_high_scores(5)

        self.screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont(None, 72)
        self.font_header = pygame.font.SysFont(None, 48)
        self.font_cell = pygame.font.SysFont(None, 36)

        # Main Menu button
        btn_width, btn_height = 250, 60
        menu_btn = Button("Main Menu", Screen.WIDTH//2 - btn_width//2, 500, btn_width, btn_height, self.exit)
        self.button_group = ButtonGroup([menu_btn])

        # Overlay
        self.overlay = pygame.Surface((Screen.WIDTH, Screen.HEIGHT))
        self.overlay.fill((0,0,0))
        self.overlay.set_alpha(25)

    def exit(self):
        self.running = False

    def run(self):
        while self.running:
            self.clock.tick(Screen.FPS)
            self.handle_events()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.button_group.handle_event(event)

    def draw(self):
        self.screen.blit(self.background_surface, (0,0))
        self.screen.blit(self.overlay, (0,0))

        # Title
        title = self.font_title.render("GAME OVER", True, (255,0,0))
        self.screen.blit(title, (Screen.WIDTH//2 - title.get_width()//2, 50))

        # Table headers
        header_y = 180
        col_widths = [100,150,200]
        table_width = sum(col_widths) + 40
        start_x = Screen.WIDTH//2 - table_width//2

        col_score = start_x
        col_difficulty = col_score + col_widths[0] + 20
        col_date = col_difficulty + col_widths[1] + 20

        header_score = self.font_header.render("Score", True, (255,255,0))
        header_difficulty = self.font_header.render("Difficulty", True, (255,255,0))
        header_date = self.font_header.render("Date", True, (255,255,0))

        self.screen.blit(header_score, (col_score, header_y))
        self.screen.blit(header_difficulty, (col_difficulty, header_y))
        self.screen.blit(header_date, (col_date, header_y))

        pygame.draw.line(self.screen, (255,255,255), (start_x, header_y+50), (start_x+table_width, header_y+50), 2)

        # Table rows
        row_y = header_y + 70
        for entry in self.top_scores:
            score_text = self.font_cell.render(str(entry[0]), True, (255,255,255))
            difficulty_text = self.font_cell.render(str(entry[1]), True, (255,255,255))
            date_text = self.font_cell.render(str(entry[2]), True, (255,255,255))

            self.screen.blit(score_text, (col_score, row_y))
            self.screen.blit(difficulty_text, (col_difficulty, row_y))
            self.screen.blit(date_text, (col_date, row_y))
            row_y += 50

        self.button_group.draw(self.screen)
        pygame.display.flip()
