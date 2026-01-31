from .models import CircleShape, TriangleShape, Shot

import pygame, math, random

from src.utils import logging_tool

logger = logging_tool.get_logger(__name__)


class Unit(TriangleShape):
    def __init__(self,
                 x: int, y: int,
                 radius: int=5,
                 color: tuple=(255, 255, 255),
                 belonging: String = None
                 ):
        # call the parent class constructor
        super().__init__(x, y, radius, color)
        self.moving = False
        self.target = (self.position.x, self.position.y)
        self.speed = 1
        self._fire_at_will = False

        self._range = CircleShape(x, y, 20*self.radius, (255, 0, 0))
        self._show_range = False
        
        self._enemies_in_range = pygame.sprite.Group()

        self._belonging = belonging
        
        self._shots_fired = pygame.sprite.Group()

        self._drawable = pygame.sprite.Group()
        self._updatable = pygame.sprite.Group()

        self._drawable.add(self._shots_fired)
        self._updatable.add(self._shots_fired)

    def draw(self, screen):
        for object in self._drawable:
            object.draw(screen)
        if self._show_range:
            self._range.draw(screen)
        super().draw(screen)

    def step(self):
        # take a step forward
        angle = self.rotation
        rad = math.radians(angle)
        dx = self.speed * math.cos(rad)
        dy = self.speed * math.sin(rad)

        self.position.x += dx
        self.position.y += dy
    
    def _update_range_pos(self):
        self._range.set_position(self.position.x, self.position.y)
    
    def _fire_shot_at(self, x, y):
        if len(self._shots_fired) >= 1:
            return

        shot = Shot(self.position.x, self.position.y, movement_range=10)
        shot.look_at(x, y)

        self._shots_fired.add(shot)
    
    def update_fire_at_will(self):
        #logger.info(f"Fire at will: {self._fire_at_will}, enemies in range: {len(self._enemies_in_range)}")
        if self._fire_at_will and len(self._enemies_in_range) > 0:
            targets = self._enemies_in_range
            random_target = random.choice(targets)

            aim_pos = random_target.get_position()
            self._fire_shot_at(aim_pos[0], aim_pos[1])
        elif len(self._enemies_in_range) > 0:
            logger.info(f"Fire at will: {self._fire_at_will}, enemies in range: {len(self._enemies_in_range)}, unit: {self._belonging}")

    def update(self, dt):
        for object in self._updatable:
            object.update(dt)
        if self.moving:
            self._update_range_pos()
            self.look_at(self.target[0], self.target[1])
            self.step()
            if self._has_reached_target():#if self.get_position()[0] <= self.target[0] + self.radius and self.get_position()[0] >= self.target[0] - self.radius and self.get_position()[1] <= self.target[1] + self.radius and self.get_position()[1] >= self.target[1] - self.radius:
                self.moving = False
        self.update_fire_at_will()
    
    def _has_reached_target(self):
        x_in_range = self.get_position()[0] >= self.target[0] - self.radius and self.get_position()[0] <= self.target[0] + self.radius
        y_in_range = self.get_position()[1] >= self.target[1] - self.radius and self.get_position()[1] <= self.target[1] + self.radius
        if x_in_range and y_in_range:
            return True
        else:
            return False
    
    def is_enemy_unit_in_range(self, unit: Unit):
        if self._range.collides_with(unit):
            logger.info(f"Unit {self._belonging} is in range of {unit._belonging} fire_at_will is {self._fire_at_will}")
            self._enemies_in_range.add(unit)
        else:
            #logger.info(f"Unit {self._belonging} is not in range of {unit._belonging}")
            self._enemies_in_range.remove(unit)

    def move_towards(self, x, y):
        self.moving = True
        self.target = (x, y)
        self.look_at(x, y)

    def get_position(self):
        return self.position

    def get_radius(self):
        return self.radius

    def set_posistion(self, x, y):
        self.x = x
        self.y = y


    def set_fire_at_will(self, value):
        logger.info(f"Setting fire at will to {value}")
        self._fire_at_will = value
