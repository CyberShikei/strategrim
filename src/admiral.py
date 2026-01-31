import pygame

from .units import UnitStack
from .utils import logging_tool
from .rubberbandSelector import RubberBandSelector

from config import (SCREEN_WIDTH, SCREEN_HEIGHT)

DEFAULT_STACK_SPACING = 10
DEFAULT_UNIT_DENCITY = 29
DEFAULT_UNIT_RADIUS = 2

logger = logging_tool.get_logger(__name__)

BUTTON_PRESSED = pygame.USEREVENT + 10

class Admiral(pygame.sprite.Sprite):
    def __init__(self, admiral_name="player1", army_size=5, unit_color=(255, 0, 0), spawn_point=(0, 0)):
        super().__init__()
        self.running = True

        self._name = admiral_name
        self._init_army_size = army_size
        self._unit_color = unit_color

        self._selector = RubberBandSelector()

        self._unit_stacks = pygame.sprite.Group()
        self._selected_units = pygame.sprite.Group()

        self._spawn_army(spawn_point)

    def _spawn_army(self, spawn_point):
        stack_spacing = DEFAULT_STACK_SPACING
        unit_dencity = DEFAULT_UNIT_DENCITY
        unit_radius = DEFAULT_UNIT_RADIUS
        unit_spacing = stack_spacing//2
        
        army_size = self._init_army_size

        wall_padding = int(5/100*SCREEN_WIDTH)

        start_pos = (spawn_point[0] + wall_padding, spawn_point[1] + wall_padding)

        first_stack = UnitStack(*start_pos, unit_dencity, unit_radius, unit_spacing, color=self._unit_color, belonging=self._name)
        self._unit_stacks.add(first_stack)
         
        stack_spacing = int(stack_spacing/100*first_stack.get_stack_area()[2])

        for i in range(1, army_size):
            stack_pos = (start_pos[0] + first_stack.get_stack_area()[2]*i + stack_spacing, start_pos[1])
            stack = UnitStack(*stack_pos, unit_dencity, unit_radius, unit_spacing, color=self._unit_color, belonging=self._name)
            self._unit_stacks.add(stack)

    def get_name(self):
        return self._name

    def get_unit_stacks(self):
        return self.unit_stacks
    
    def get_selected_units(self):
        return self._selected_units
    
    def set_fire_at_will(self, state=False):
        for stack in self._selected_units:
            stack.set_fire_at_will(state)
    
    def set_stack_unit_density(self, state=False):
        for stack in self._selected_units:
            stack.set_stack_unit_density(state)

    def has_selected_fire_at_will(self):
        for stack in self._selected_units:
            if stack.is_fire_at_will():
                return True
        return False
    
    def has_selected_stack_unit_density(self):
        for stack in self._selected_units:
            if stack.dense():
                return True
        return False

    def is_selected(self):
        if len(self._selected_units) > 0:
            return True
        else:
            return False

    def update(self, dt):
        if not self.running:
            return

        if is_left_click():
            button_pressed = False
            for event in pygame.event.get():
                if event.type == BUTTON_PRESSED:
                    button_pressed = True
            if not button_pressed:
                self._selector.activate()
                for stack in self._unit_stacks:
                    if stack.is_in_area(self._selector.get_rect_points()):
                        stack.select()
                        self._selected_units.add(stack)
                    else:
                        stack.deselect()
                        self._selected_units.remove(stack)
                    self._selector.update(dt)
        elif not is_left_click():
            self._selector.deactivate()

        for stack in self._unit_stacks:
            stack.update(dt)

    def draw(self, screen):
        if not self.running:
            return
        
        if self._selector.isActive():
            self._selector.draw(screen)

        for stack in self._unit_stacks:
            stack.draw(screen)
    
def is_left_click(): return pygame.mouse.get_pressed()[0]

