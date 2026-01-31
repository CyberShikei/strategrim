import pygame

from .triangleShape import TriangleShape

from src.utils import logging_tool

logger = logging_tool.get_logger(__name__)

class Shot(TriangleShape):
    def __init__(self, x, y, radius=1, color=(255, 255, 255), movement_range=10):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__(x, y, radius, color)
        
        self.active = True

        self.moving = False
        self.target = (x, y)
        self.speed = 10

        self._movement_range = movement_range

        logger.info("Shot created")
        


    def step(self):
        # take a step forward
        angle = self.rotation
        rad = math.radians(angle)
        dx = self.speed * math.cos(rad)
        dy = self.speed * math.sin(rad)

        self.position.x += dx
        self.position.y += dy

        self._movement_range -= 1
        if self._movement_range <= 0:
            self.active = False

    def destroy(self):
        self.active = False

    def draw(self, screen):
        if self.active:
            super().draw(screen)

    def update(self, dt):
        if self.active:
            self.step()



