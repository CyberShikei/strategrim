import pygame

from src.utils import logging_tool

from config import (SCREEN_WIDTH, SCREEN_HEIGHT, RESOURCES, IMAGES, IMAGE_EXTENTION)

logger = logging_tool.get_logger(__name__)

BUTTON_PRESSED = pygame.USEREVENT + 10

class Banner(pygame.sprite.Sprite):
    def __init__(self, banner_name ,image_path, x, y, width=None, height=None, background=(0, 0, 0)):
        super().__init__()
        self._name = banner_name
        self._image = pygame.image.load(f"{RESOURCES}/{IMAGES}/{image_path}.{IMAGE_EXTENTION}")
        self._background = background
        
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
    def __init__(self, button_name, image_path, x, y, trigger_event=None, width=None, height=None, background=(0, 0, 0), py_event=True, cooldown=20, active=True, toggle=False, toggle_state=False):
        super().__init__()
        self._name = button_name
        
        self._image = None
        self._image_path = image_path
        
        self._toggle = toggle
        self._toggle_state = toggle_state
        #if not image_path or image_path == "":
        #    self._image_path = f"{RESOURCES}/{IMAGES}/blank_button.{IMAGE_EXTENTION}"
        
        self._width = width
        self._height = height
        self._rect = pygame.Rect(x, y, self._width, self._height)
        self._rect.x = x
        self._rect.y = y

        self._load_image()
        
        #self._image = pygame.image.load(f"{RESOURCES}/{IMAGES}/{self._image_path}.{IMAGE_EXTENTION}")

        self._background = background
        self._trigger_event = trigger_event
        self._py_event = py_event
        self._cooldown = cooldown
        self._counter_cooldown = cooldown

        self._active = active
    
    def _load_image(self):
        if not self._image_path or self._image_path == "":
            self._image_path = f"blank_button"
        if self._toggle:
            self._image_path = f"{self._image_path}"[:-1]
            if self._toggle_state == True:
                self._image_path = f"{self._image_path}1"
            else:
                self._image_path = f"{self._image_path}0"

        self._image = pygame.image.load(f"{RESOURCES}/{IMAGES}/{self._image_path}.{IMAGE_EXTENTION}")
        
        width, height = self._width, self._height
        x, y = self._rect.x, self._rect.y

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

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False
    
    def is_active(self):
        return self._active

    def activate_toggle_state(self):
        if self.is_active():
            self._toggle_state = True
        self._load_image()

    def deactivate_toggle_state(self):
        if self.is_active():
            self._toggle_state = False
        self._load_image()
        
    def is_toggled(self):
        return self._toggle_state

    def is_toggle(self):
        return self._toggle
    
    def toggle_state(self):
        self._toggle_state = not self._toggle_state
        self._load_image()

    def update(self, dt):
        if not self._active:
            self._background = (50, 50, 50)
            return
        if self._rect.collidepoint(pygame.mouse.get_pos()):
            pygame.event.post(pygame.event.Event(BUTTON_PRESSED))
            self._background = (175, 0, 0)
            if self.is_left_clicked() and self._counter_cooldown <= 0:
                #pygame.event.post(pygame.event.Event(BUTTON_PRESSED))
                self._counter_cooldown = 100
                if self._py_event:
                    pygame.event.post(pygame.event.Event(self._trigger_event))
                elif self.is_toggle():
                    #self._toggle_state = not self._toggle_state
                    self.toggle_state()
                    self._trigger_event(state=self._toggle_state)
                else:
                    self._trigger_event()
            elif self._counter_cooldown > 50:
                self._background = (150, 150, 150)
        else:
            self._background = (175, 125, 0)

        self._counter_cooldown -= 1
    def draw(self, screen):
        pygame.draw.rect(screen, self._background, self._rect)
        screen.blit(self._image, self._rect)
    
    def get_id(self):
        return self._name

    def is_left_clicked(self):
        if self._trigger_event:
            if pygame.mouse.get_pressed()[0]:
                return True

