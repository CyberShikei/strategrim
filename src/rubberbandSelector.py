#!./.venv/bin/python

import pygame

class RubberBandSelector(pygame.sprite.Sprite):
    def __init__(self, color=(255, 255, 255), thickness=2):
        self.color = color
        self.thickness = thickness
        self.anchor = None
        self.selection_rect = None
        self.active = False

    def isActive(self):
        return self.active

    def activate(self):
        if self.active:
            return
        pos = pygame.mouse.get_pos()
        self.anchor = pos
        self.selection_rect = pygame.Rect(pos[0], pos[1], 0, 0)
        self.active = True

    def deactivate(self):
        self.active = False

    def update(self, dt):
        """Handles mouse events to manage the selection box."""
        pos = pygame.mouse.get_pos()
        if self.active:
            if pos[0] > self.anchor[0]:
                self.selection_rect.width = pos[0] - self.anchor[0]
            else:
                self.selection_rect.x = pos[0]
                self.selection_rect.width = self.anchor[0] - pos[0]

            if pos[1] > self.anchor[1]:
                self.selection_rect.height = pos[1] - self.anchor[1]
            else:
                self.selection_rect.y = pos[1]
                self.selection_rect.height = self.anchor[1] - pos[1]


    def draw(self, screen):
        """Draws the selector box if active."""
        if self.active:
            pygame.draw.rect(screen, self.color, self.selection_rect, self.thickness)

    def get_rect_points(self):
        x1 = self.selection_rect.x
        y1 = self.selection_rect.y

        x2 = x1 + self.selection_rect.width
        y2 = y1 + self.selection_rect.height

        return x1, y1, x2, y2

