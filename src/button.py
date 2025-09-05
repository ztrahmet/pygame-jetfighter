# -*- coding: utf-8 -*-
"""
button.py

Reusable button widgets for Jet Fighter.

This module defines:
    - :class:`Button`: a clickable button with mouse and keyboard support.
    - :class:`ButtonGroup`: a container for managing multiple buttons
      with navigation (arrow keys) and selection (Enter key).
"""

from __future__ import annotations

import pygame


class Button:
    """
    Interactive button for menus.

    Supports mouse hover, click, and keyboard selection.
    """

    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        width: int,
        height: int,
        callback,
        font_size: int = 36,
        color_idle: tuple[int, int, int] = (50, 50, 50),
        color_hover: tuple[int, int, int] = (100, 100, 100),
        color_selected: tuple[int, int, int] = (150, 150, 150),
        text_color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        """
        Initialize the button.

        Args:
            text (str): Button label.
            x (int): X-coordinate of top-left corner.
            y (int): Y-coordinate of top-left corner.
            width (int): Button width.
            height (int): Button height.
            callback (Callable): Function executed when button is activated.
            font_size (int): Size of text font.
            color_idle (tuple): Background color when idle.
            color_hover (tuple): Background color when hovered.
            color_selected (tuple): Background color when selected.
            text_color (tuple): Text color.
        """
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback

        # Colors
        self.color_idle = color_idle
        self.color_hover = color_hover
        self.color_selected = color_selected
        self.text_color = text_color

        # Font
        self.font = pygame.font.SysFont(None, font_size)

        # Selection state (used for keyboard navigation)
        self.selected = False

    # ---------------- Drawing ----------------
    def draw(self, surface: pygame.Surface) -> None:
        """Render the button to the given surface."""
        mouse_pos = pygame.mouse.get_pos()

        # Determine background color
        if self.selected:
            color = self.color_selected
        elif self.rect.collidepoint(mouse_pos):
            color = self.color_hover
        else:
            color = self.color_idle

        # Draw button background
        pygame.draw.rect(surface, color, self.rect, border_radius=10)

        # Draw centered text
        text_surf = self.font.render(self.text, True, self.text_color)
        surface.blit(
            text_surf,
            (
                self.rect.centerx - text_surf.get_width() // 2,
                self.rect.centery - text_surf.get_height() // 2,
            ),
        )

    # ---------------- Event Handling ----------------
    def handle_mouse_event(self, event: pygame.event.Event) -> None:
        """Handle mouse clicks to trigger the callback."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()


class ButtonGroup:
    """
    Manage a collection of :class:`Button` objects.

    Supports keyboard navigation (Up/Down) and selection (Enter).
    """

    def __init__(self, buttons: list[Button]) -> None:
        """
        Initialize the button group.

        Args:
            buttons (list[Button]): List of buttons to manage.
        """
        self.buttons = buttons
        self.selected_index = 0

        # Mark first button as selected by default
        if self.buttons:
            self.buttons[0].selected = True

    # ---------------- Event Handling ----------------
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle keyboard and mouse events for all buttons."""
        # Mouse interaction
        for btn in self.buttons:
            btn.handle_mouse_event(event)

        # Keyboard navigation
        if event.type == pygame.KEYDOWN and self.buttons:
            # Deselect current button
            self.buttons[self.selected_index].selected = False

            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                self.buttons[self.selected_index].callback()

            # Select new button
            self.buttons[self.selected_index].selected = True

    # ---------------- Drawing ----------------
    def draw(self, surface: pygame.Surface) -> None:
        """Draw all buttons to the given surface."""
        for btn in self.buttons:
            btn.draw(surface)
