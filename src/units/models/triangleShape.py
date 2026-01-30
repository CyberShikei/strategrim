import pygame, math

# Base class for game objects


class TriangleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color=(255, 255, 255)):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

        self.rotation = 0

        self.color = color

    def draw(self, screen):
        triangle = self.triangle()
        pygame.draw.polygon(screen, self.color, triangle)

    def triangle(self):
       # forward = pygame.Vector2(0, -1).rotate(self.rotation)
       # right = pygame.Vector2(0, 1).rotate(
       #     self.rotation + 90) * self.radius / 1.5
       # a = self.position + forward * self.radius
       # b = self.position - forward * self.radius - right
       # c = self.position - forward * self.radius + right
        radius = self.radius
        center = self.position
        start_angle = math.radians(self.rotation)
        points = []

        for i in range(3):
            # 120 degrees = 2 * PI / 3 radians
            angle = start_angle + i * (2 * math.pi / 3)
        
            # Calculate x, y using cosine and sine
            x = center.x + radius * math.cos(angle)
            y = center.y + radius * math.sin(angle)
            points.append(pygame.math.Vector2(x, y))

        return points
    
    def look_at(self, x, y):
        dx = x - self.position.x
        dy = y - self.position.y

        rads = math.atan2(dy, dx)
        angle = math.degrees(rads) % 360

        self.rotation = angle

    def rotate(self, angle):
        self.rotation += angle
        self.rotation %= 360

    def update(self, dt):
        self.position += self.velocity * dt

    def get_radius(self):
        return self.radius

    def colides_with(self, other):
        dist = self.position.distance_to(other.position)
        condition = dist < self.radius + other.radius
        return condition

    def set_color(self, color):
        self.color = color

    def set_position(self, x, y):
        self.position = pygame.Vector2(x, y)

