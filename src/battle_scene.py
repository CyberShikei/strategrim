import pygame

from .units import UnitStack
from .rubberbandSelector import RubberBandSelector
from .utils import Banner, Button

from config import (SCREEN_WIDTH, SCREEN_HEIGHT)

MAIN_MENU = pygame.USEREVENT + 1

class BattleScene(pygame.sprite.Sprite):
    def __init__(self):
        print("BattleScene")
        super().__init__()
        self.running = True
        self.background = None

        self._selector = RubberBandSelector()

        self._updatable = pygame.sprite.Group()
        self._drawable = pygame.sprite.Group()
        
        self._unit_stacks = pygame.sprite.Group()

        self._create_ui()

    def _create_ui(self):
        # Menu Buttoni
        spacing = 1
        button_size = int((3*spacing)/100*SCREEN_WIDTH), int((3*spacing)/100*SCREEN_WIDTH)
        b_menu_pos = int(SCREEN_WIDTH - (button_size[0] + (1*spacing)/100*SCREEN_WIDTH)), int((1*spacing)/100*SCREEN_WIDTH)
        b_menu = Button("bMenu", "resources/images/menu.bmp", *b_menu_pos, MAIN_MENU, *button_size, (175, 125, 0))
        
        # Spawn Unit Button
        b_spawn_unit_pos = int(SCREEN_WIDTH - (button_size[0] + (1*spacing)/100*SCREEN_WIDTH)), int((((1*spacing)/100*SCREEN_WIDTH)) + 50)
        b_spawn_unit = Button("bSpawnUnit", "resources/images/spawn.bmp", *b_spawn_unit_pos, self.spawn_unit, *button_size, (175, 125, 0), py_event=False)

        self._updatable.add(b_menu, b_spawn_unit)
        self._drawable.add(b_menu, b_spawn_unit)

    
    def spawn_unit(self, x=0, y=0):
        if not self.running:
            return
        sx, sy = 0, 0
        if x == 0 and y == 0:
            sx, sy = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
        self._unit_stacks.add(UnitStack(x=sx, y=sy, unit_count=29))
        self._updatable.add(self._unit_stacks)
        self._drawable.add(self._unit_stacks)
        print(f"Spawned unit {self._unit_stacks}")

    def update(self, dt):
        if not self.running:
            return
        self.is_left_mouse_down()
        self._selector.update(dt)
        if self._selector.active:
            for object in self._unit_stacks:
                if object.is_in_area(self._selector.get_rect_points()):
                    object.select()
                else:
                    object.deselect()
                
        for object in self._updatable:
            object.update(dt)

    def draw(self, screen):
        if not self.running:
            return
        self._selector.draw(screen)

        for object in self._drawable:
            object.draw(screen)
        
    def deactivate(self):
        self.running = False

    def is_left_mouse_down(self):
        if pygame.mouse.get_pressed()[0]:
            self._selector.activate()
        elif not pygame.mouse.get_pressed()[0]:
            self._selector.deactivate()
