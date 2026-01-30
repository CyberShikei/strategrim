#!./.venv/bin/python

import pygame
#import pygame.freetype

from config import (GAME_TITLE, SCREEN_HEIGHT,
    SCREEN_WIDTH)

#pygame.freetype.init()
#MY_FONT = pygame.freetype.SysFont('Arial', 24)

class MainMenuScene(pygame.sprite.Sprite):
    _updatable = pygame.sprite.Group()
    _drawable = pygame.sprite.Group()

    def __init__(self):
        super().__init__()
        self.running = True
        self.objects = pygame.sprite.Group()
        self.background = None
        
        self._create_objects()

    def _create_objects(self):
        # Title
        banner_size = int(80/100*SCREEN_WIDTH), 0#int(20/100*SCREEN_HEIGHT)
        banner = Banner("resources/images/title.bmp", SCREEN_WIDTH//2-banner_size[0]//2, int(0/100*SCREEN_HEIGHT), *banner_size)
        
        button_size = int(20/100*SCREEN_WIDTH), int(10/100*SCREEN_HEIGHT)
        # Start Game Button
        start_button = Button("resources/images/start.bmp", SCREEN_WIDTH//2-button_size[0]//2, int(40/100*SCREEN_HEIGHT), None, *button_size, (175, 125, 0))
        # Quit Game Button
        quit_button = Button("resources/images/quit.bmp", SCREEN_WIDTH//2-button_size[0]//2, int(60/100*SCREEN_HEIGHT), pygame.QUIT, *button_size, (175, 125, 0))

        #self.objects.add(banner)
        #self.objects.add(start_button)
        #self.objects.add(quit_button)

        self._updatable.add(start_button, quit_button)
        self._drawable.add(banner, start_button, quit_button)

    def update(self, dt):
        #quit_button = Button("Quit Game", 50, (255, 255, 255), (SCREEN_WIDTH/2, 400))
        for object in self._updatable:
            object.update()

    def draw(self, screen):
        for object in self._drawable:
            object.draw(screen)

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
    def __init__(self, image_path, x, y, trigger_event=None, width=None, height=None, background=(0, 0, 0)):
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

        self._background = background
        self._trigger_event = trigger_event

    def update(self):
        if self._rect.collidepoint(pygame.mouse.get_pos()):
            self._background = (175, 0, 0)
            if self.is_left_clicked():
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
        

