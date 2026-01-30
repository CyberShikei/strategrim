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
    def __init__(self, button_name, image_path, x, y, trigger_event=None, width=None, height=None, background=(0, 0, 0)):
        super().__init__()
        self._name = button_name
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

        self._background = background
        self._trigger_event = trigger_event

    def update(self):
        if self._rect.collidepoint(pygame.mouse.get_pos()):
            self._background = (175, 0, 0)
            if self.is_left_clicked():
                print(f"Button {self._name} clicked")
                pygame.event.post(pygame.event.Event(self._trigger_event))
        else:
            self._background = (175, 125, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self._background, self._rect)
        screen.blit(self._image, self._rect)

    def is_left_clicked(self):
        if self._trigger_event:
            if pygame.mouse.get_pressed()[0]:
                return True

