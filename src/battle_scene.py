import pygame

from .units import UnitStack
from .rubberbandSelector import RubberBandSelector
from .utils import Banner, Button, logging_tool

from config import (SCREEN_WIDTH, SCREEN_HEIGHT)

logger = logging_tool.get_logger(__name__)

MAIN_MENU = pygame.USEREVENT + 1

_button_padding = 1

class BattleScene(pygame.sprite.Sprite):
    def __init__(self):
        logger.info("Initializing Battle Scene")

        super().__init__()
        self.running = True
        self.background = None

        self._selector = RubberBandSelector()

        self._updatable = pygame.sprite.Group()
        self._drawable = pygame.sprite.Group()
        self._selected_unit = pygame.sprite.Group()

        self._unit_stacks = pygame.sprite.Group()
        self._unit_action_buttons = pygame.sprite.Group()

        self._create_ui()

    def _create_ui(self):
        # Menu Buttoni
        spacing = _button_padding
        button_size = int((3*spacing)/100*SCREEN_WIDTH), int((3*spacing)/100*SCREEN_WIDTH)
        b_menu_pos = int(SCREEN_WIDTH - (button_size[0] + (1*spacing)/100*SCREEN_WIDTH)), int((1*spacing)/100*SCREEN_WIDTH)
        b_menu = Button("bMenu", "resources/images/menu.bmp", *b_menu_pos, MAIN_MENU, *button_size, (175, 125, 0))
        
        # Spawn Unit Button
        b_spawn_unit_pos = int(SCREEN_WIDTH - (button_size[0] + (1*spacing)/100*SCREEN_WIDTH)), int((((1*spacing)/100*SCREEN_WIDTH)) + 50)
        b_spawn_unit = Button("bSpawnUnit", "resources/images/spawn.bmp", *b_spawn_unit_pos, self.spawn_unit, *button_size, (175, 125, 0), py_event=False)
        
        self._create_unit_action_bar()
        
        self._updatable.add(b_menu, b_spawn_unit)
        self._drawable.add(b_menu, b_spawn_unit)
    
    def _create_unit_action_bar(self):
        # Unit Action Bar
        
        width_perc, height_perc = 100, 10
        ban_bar_size = int(width_perc/100*SCREEN_WIDTH), int(height_perc/100*SCREEN_HEIGHT)
        ban_bar_pos = 0, SCREEN_HEIGHT - ban_bar_size[1]
        ban_unit_action_bar = Banner("banUnitActionBar", "resources/images/action_bar.bmp", *ban_bar_pos, *ban_bar_size)
        
        # Unit Action Buttons
        spacing = int(_button_padding/100*SCREEN_WIDTH)
        button_square = int((3*spacing))
        button_size = button_square, button_square
        b_toggle_stack_density = Button("bToggleStackDensity", "resources/images/stack_formation.bmp", spacing, ban_bar_pos[1] + (button_size[1]//2) , None, *button_size, (175, 125, 0), py_event=False, active=False)
        
        b_toggle_fire_at_will = Button("bToggleFireAtWill", "resources/images/fire_at_will0.bmp", spacing*2 + button_size[0], ban_bar_pos[1] + (button_size[1]//2), None, *button_size, (175, 125, 0), py_event=False, active=False)

        self._unit_action_buttons.add(b_toggle_stack_density, b_toggle_fire_at_will)

        self._updatable.add(self._unit_action_buttons)
        self._drawable.add(ban_unit_action_bar, self._unit_action_buttons)
    
    

    def _activate_unit_action_buttons(self):
        for button in self._unit_action_buttons:
            button.activate()

    def _deactivate_unit_action_buttons(self):
        for button in self._unit_action_buttons:
            button.deactivate()
    
    def _has_selected_units(self):
        return len(self._selected_unit) > 0

    def spawn_unit(self, x=0, y=0):
        if not self.running:
            return
        sx, sy = 0, 0
        if x == 0 and y == 0:
            sx, sy = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
        self._unit_stacks.add(UnitStack(x=sx, y=sy, unit_count=19, unit_radius=2))
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
                    self._selected_unit.add(object)
                    if self._has_selected_units():
                        self._activate_unit_action_buttons()
                    object.select()
                else:
                    self._selected_unit.remove(object)
                    self._deactivate_unit_action_buttons()
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
