import pygame

from units import Raider

from config import (SCREEN_HEIGHT,
                       SCREEN_WIDTH)


class BattleField(pygame.sprite.Sprite):
    def __init__(self):
        # initialize the field
        self.raider = Raider(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.spawn_timer = 0.0

    def update(self, dt):
        self.raider.update(dt)
        # updates on tick
