import pygame

from src.utils import logging_tool
from src.shapes import RectangleShape

from config import (SCREEN_WIDTH, SCREEN_HEIGHT, RESOURCES, IMAGES, IMAGE_EXTENTION)

logger = logging_tool.get_logger(__name__)

BUTTON_PRESSED = pygame.USEREVENT + 10

class Banner(RectangleShape):
    def __init__(self, #banner_name ,image_path, x, y, width=None, height=None, background=(0, 0, 0)):
                 x: int = 0,
                 y: int = 0,
                 width: int = 0,
                 height: int = 0,
                 background_color: tuple = (0, 0, 0),
                 banner_id: Str = '',
                 image_path: Str = ''
                 ):
        super().__init__(x, y, width, height, background_color)
        logger.debug(f"Creating Banner: {banner_id}")
        self._id = banner_id

        self._image = None
        self._image_path = image_path
        self._background_color = background_color
    
    def _get_image_path(self):
        if not self._image_path or self._image_path == "":
            self._image_path = f"blank_button"
        image_path = f"{RESOURCES}/{IMAGES}/{self._image_path}.{IMAGE_EXTENTION}"
        return image_path

    def _load_image(self):
        image_path = self._get_image_path()
        try:
            logger.debug(f"Loading Image: {image_path}")
            self._image = pygame.image.load(f"{image_path}")
            logger.debug(f"Image loaded: {image_path}")
        except Exception as e:
            logger.error(e)

        width, height = self._width, self._height
        x, y = self._x, self._y

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
        
        # Transform Image
        try:
            self._image = pygame.transform.scale(self._image, (self._width, self._height)) 
        except Exception as e:
            logger.error(e)
        

    def update(self):
        pass

    def draw(self, screen):
        if not self._image:
            self._load_image()
        screen.blit(self._image, self.get_rect())


class Button(Banner):
    def __init__(self,
                    active: bool = True,
                    toggle: bool = False,
                    toggle_state: bool = False,
                    py_event: bool = True,
                    x: int = 0,
                    y: int = 0,
                    width: int = 0,
                    height: int = 0,
                    cooldown: int = 20,
                    background_color: tuple = (0, 0, 0),
                    button_id: Str = '',
                    image_path: Str = '',
                    trigger_event: callable = None
                 ):
        super().__init__(x, y, width, height, background_color, button_id, image_path)
        self._id = button_id
        logger.debug(f"Creating Button: {button_id}")

        self._toggle = toggle
        self._toggle_state = toggle_state
        
        self._load_image()
        
        self._trigger_event = trigger_event
        self._py_event = py_event
        self._cooldown = cooldown
        self._counter_cooldown = cooldown

        self._active = active


    def _get_image_path(self):
        if not self._image_path or self._image_path == "":
            self._image_path = f"blank_button"
        if self.is_toggle():
            self._image_path = f"{self._image_path}"[:-1]
            if self._toggle_state == True:
                self._image_path = f"{self._image_path}1"
            else:
                self._image_path = f"{self._image_path}0"
        image_path = f"{RESOURCES}/{IMAGES}/{self._image_path}.{IMAGE_EXTENTION}"
        return image_path

    def _load_image(self):
        image_path = self._get_image_path()
        super()._load_image()
        
    def set_trigger_event(self, trigger_event):
        self._trigger_event = trigger_event

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False
    
    def is_active(self):
        return self._active

    def is_toggled(self):
        return self._toggle_state
   
    def _get_toggle(self):
        return self._toggle

    def is_toggle(self):
        if self._get_toggle():
            return True
        else:
            return False
    
    def toggle_state(self):
        self._toggle_state = not self._toggle_state
        self._load_image()

    def update(self, dt):
        if self._width <= 0 or self._height <= 0:
            return
        if not self._active:
            self._background = (50, 50, 50)
            return
        if self.collide_point(pygame.mouse.get_pos()):
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
        if not self._image:
            self._load_image()
        pygame.draw.rect(screen, self._background, self.get_rect())
        super().draw(screen)
        #screen.blit(self._image, self.get_rect())
    
    def get_id(self):
        return self._button_id

    def is_left_clicked(self):
        if self._trigger_event:
            if pygame.mouse.get_pressed()[0]:
                return True

