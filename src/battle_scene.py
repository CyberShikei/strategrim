import pygame

from .units import UnitStack
from .rubberbandSelector import RubberBandSelector

class BattleScene(pygame.sprite.Sprite):
    def __init__(self):
        print("BattleScene")
        super().__init__()
        self.running = True
        self.background = None

        self._selector = RubberBandSelector()

    def update(self, dt):
        if not self.running:
            return
        self.is_left_mouse_down()
        self._selector.update()

    def draw(self, screen):
        if not self.running:
            return
        self._selector.draw(screen)
        
    def deactivate(self):
        self.running = False

    def is_left_mouse_down(self):
        if pygame.mouse.get_pressed()[0]:
            self._selector.activate()
        elif not pygame.mouse.get_pressed()[0]:
            self._selector.deactivate()
