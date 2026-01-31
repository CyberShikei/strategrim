import pygame
import math, random

from .unit import Unit

class UnitStack(pygame.sprite.Sprite):
    def __init__(self,
                 x: int = 0, y: int = 0,
                 unit_count: int = 1,
                 unit_radius: int = 5,
                 spacing: int = 5,
                 color: tuple = (255, 255, 255),
                 belonging: String = None
                 ):
        
        super().__init__()
        self.x = x
        self.y = y
        self.unit_count = unit_count
        self.unit_radius = unit_radius
        
        self._density = True
        
        self._default_spacing = spacing * self.unit_radius
        self.spacing = self._default_spacing
        self.color = color
        self._belonging = belonging
        
        self._fire_at_will = False

        self.units = []#pygame.sprite.Group()
        self.spawn()

        self._selected = False
    
    def _determine_spacing(self):
        if self._density:
            self.spacing = self._default_spacing
        else:
            self.spacing = self._default_spacing * 2

    def set_stack_unit_density(self, state=False):
        if not (self._density == state):

            self._density = state
            self._determine_spacing()
            self.move_towards(self.x, self.y)

    def is_in_area(self, rect_area: tuple=(0, 0, 0, 0)):
        for unit in self.units:
            unit_pos = unit.get_position()
            if rect_area[0] < unit_pos[0] < rect_area[2] and rect_area[1] < unit_pos[1] < rect_area[3]:
                return True
        return False

    def select(self):
        self._selected = True
        self.change_color((0, 255, 0))

    def deselect(self):
        self._selected = False
        self.change_color(self.color)

    def spawn(self):
        square, extra = calcSquare(self.unit_count)
        for i in range(square):
            for j in range(square):
                self.units.append(Unit(self.x + i*self.spacing, self.y + j*self.spacing, radius=self.unit_radius, color=self.color))

        for i in range(extra):
            self.units.append(Unit(self.x + (i*self.spacing) + (square - extra)*self.spacing//2, self.y + square*self.spacing, radius=self.unit_radius, color=self.color))

    def draw(self, screen):
        for unit in self.units:
            unit.draw(screen)

    def update(self, dt):
        #self._determine_spacing()
        if self._selected and self._is_right_click():
            self.move_towards(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        self._update_xy()
        for unit in self.units:
            unit.update(dt)

    def _update_xy(self):
       self.x = self.units[0].get_position()[0]
       self.y = self.units[0].get_position()[1]
    
    def change_color(self, color):
        for unit in self.units:
            unit.set_color(color)

    def move_towards(self, x, y):
        if not self._selected:
            return
        random.shuffle(self.units)
        square, extra = calcSquare(self.unit_count)

        i, j, count = 0, 0, 0
        for unit in self.units:
            count += 1
            if not count > square*square:
                unit.move_towards(x + (i*self.spacing), y + (j*self.spacing))
                i += 1
                if i == square:
                    i = 0
                    j += 1
            elif count > square*square and i > extra:
                i = 0
            else:
                targ_x = x + (i*self.spacing) + (square - extra)*self.spacing//2
                targ_y = y + square*self.spacing
                unit.move_towards(targ_x, targ_y)
                i += 1

        #for i in range(square):
        #    for j in range(square):
        #        self.units[i].move_towards(x + (i*self.spacing), y + (j*self.spacing))

        #for i in range(extra):
        #    self.units[i][0].move_towards(x + (i*self.spacing) + (square - extra)*self.spacing//2, y - self.spacing)
    
    def _is_right_click(self):
        if pygame.mouse.get_pressed()[2]:
            return True
        else:
            return False
    
    def set_fire_at_will(self, value):
        self._fire_at_will = value
        for unit in self.units:
            unit.set_fire_at_will(value)

    def is_fire_at_will(self):
        return self._fire_at_will

    def get_stack_area(self):
        width = (self.spacing + self.unit_radius)*calcSquare(self.unit_count)[0]
        height = (self.spacing + self.unit_radius)*calcSquare(self.unit_count)[0]

        return (self.x, self.y, width, height)
    
    def belongs_to(self):
        return self._belonging
    
    def dense(self):
        return self._density
def calcSquare(i):
    int_sqrt = math.isqrt(i)
    int_sqrt_squared = int_sqrt * int_sqrt
    difference = i - int_sqrt_squared

    return int(int_sqrt), int(difference)

