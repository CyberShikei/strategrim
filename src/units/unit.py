from .models import CircleShape, TriangleShape

import pygame, math

# Player class


class Unit(TriangleShape):
    def __init__(self,
                 x, y,
                 radius=5
                 ):
        # call the parent class constructor
        super().__init__(x, y, radius)
        self.moving = False
        self.target = (self.position.x, self.position.y)
        self.speed = 1
    
    
    def step(self):
        # take a step forward
        angle = self.rotation
        rad = math.radians(angle)
        dx = self.speed * math.cos(rad)
        dy = self.speed * math.sin(rad)

        self.position.x += dx
        self.position.y += dy

    def update(self, dt):
        if self.moving:
            self.look_at(self.target[0], self.target[1])
            self.step()
            if self.get_position()[0] <= self.target[0] + self.radius and self.get_position()[0] >= self.target[0] - self.radius and self.get_position()[1] <= self.target[1] + self.radius and self.get_position()[1] >= self.target[1] - self.radius:
                self.moving = False

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
