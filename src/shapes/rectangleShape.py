import pygame

from config import (SCREEN_WIDTH, SCREEN_HEIGHT)

from src.utils import logging_tool

logger = logging_tool.get_logger(__name__)

class RectangleShape(pygame.sprite.Sprite):
    def __init__(self,
                 x: int, y: int, width: int, height: int, color: tuple = (255, 255, 255)):
        super().__init__()
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._color = color
    
    def get_rect(self):
        return (self._x, self._y, self._width, self._height)

    def collide_point(self, point):
        return self._x < point[0] < self._x + self._width and self._y < point[1] < self._y + self._height

    def draw(self, screen):
        try:
            pygame.draw.rect(screen, self._color, (self._x, self._y, self._width, self._height))
        except Exception as e:
            logger.error(e)

    def update(self):
        pass
