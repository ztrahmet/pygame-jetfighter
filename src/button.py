"""
button.py

Reusable button class with keyboard and mouse support.
"""

import pygame

class Button:
    """Interactive button for Pygame with mouse and keyboard support."""

    def __init__(self, text, x, y, width, height, callback,
                 font_size=36,
                 color_idle=(50, 50, 50),
                 color_hover=(100, 100, 100),
                 color_selected=(150, 150, 150),
                 text_color=(255, 255, 255)):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.color_idle = color_idle
        self.color_hover = color_hover
        self.color_selected = color_selected
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, font_size)
        self.selected = False

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.selected:
            color = self.color_selected
        elif self.rect.collidepoint(mouse_pos):
            color = self.color_hover
        else:
            color = self.color_idle

        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        text_surf = self.font.render(self.text, True, self.text_color)
        surface.blit(
            text_surf,
            (self.rect.centerx - text_surf.get_width() // 2,
             self.rect.centery - text_surf.get_height() // 2)
        )

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

class ButtonGroup:
    """Manages a group of buttons with keyboard and mouse navigation."""

    def __init__(self, buttons):
        self.buttons = buttons
        self.selected_index = 0
        if buttons:
            self.buttons[0].selected = True

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_mouse_event(event)

        if event.type == pygame.KEYDOWN:
            self.buttons[self.selected_index].selected = False

            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                self.buttons[self.selected_index].callback()

            self.buttons[self.selected_index].selected = True

    def draw(self, surface):
        for btn in self.buttons:
            btn.draw(surface)
