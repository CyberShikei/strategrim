import pygame

class Banner(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, width=None, height=None, background=(0, 0, 0)):
        super().__init__()
        self._image = pygame.image.load(image_path)
        
        if width and height:
            self._width = width
            self._height = height
        elif width and not height:
            scale = width/self._image.get_width()
            self._width = width
            self._height = self._image.get_height()*scale
        elif not width and height:
            scale = height/self._image.get_height()
            self._width = self._image.get_width()*scale
            self._height = height
        else:
            self._width = self._image.get_width()
            self._height = self._image.get_height()

        self._image = pygame.transform.scale(self._image, (self._width, self._height))
        self._rect = self._image.get_rect()
        self._rect.x = x
        self._rect.y = y
    
    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self._image, self._rect)


class Button(pygame.sprite.Sprite):
    def __init__(self, button_name, image_path, x, y, trigger_event=None, width=None, height=None, background=(0, 0, 0), py_event=True, cooldown=20):
        super().__init__()
        self._name = button_name
        print(f"creating button {self._name} at {x}, {y}")
        if not image_path or image_path == "":
            image_path = "resources/images/blank_button.bmp"
        self._image = pygame.image.load(image_path)
        
        if width and height:
            self._width = width
            self._height = height
        elif width and not height:
            scale = width /self._image.get_width()
            self._width = width
            self._height = self._image.get_height()*scale
        elif not width and height:
            scale = height/self._image.get_height()
            self._width = self._image.get_width()*scale
            self._height = height
        else:
            self._width = self._image.get_width()
            self._height = self._image.get_height()

        self._image = pygame.transform.scale(self._image, (self._width, self._height))
        self._rect = self._image.get_rect()
        self._rect.x = x
        self._rect.y = y

        self._background = background
        self._trigger_event = trigger_event
        self._py_event = py_event
        self._cooldown = cooldown
        self._counter_cooldown = cooldown
    def update(self, dt):
        if self._rect.collidepoint(pygame.mouse.get_pos()):
            self._background = (175, 0, 0)
            if self.is_left_clicked() and self._counter_cooldown <= 0:
                self._counter_cooldown = 100
                print(f"Button {self._name} clicked")
                if self._py_event:
                    pygame.event.post(pygame.event.Event(self._trigger_event))
                else:
                    self._trigger_event()
        else:
            self._background = (175, 125, 0)

        self._counter_cooldown -= 1
    def draw(self, screen):
        pygame.draw.rect(screen, self._background, self._rect)
        screen.blit(self._image, self._rect)

    def is_left_clicked(self):
        if self._trigger_event:
            if pygame.mouse.get_pressed()[0]:
                return True

