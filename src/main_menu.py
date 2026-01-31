#!./.venv/bin/python

import pygame
#import pygame.freetype

from .utils import Button, Banner, logging_tool

from config import (GAME_TITLE, SCREEN_HEIGHT,
    SCREEN_WIDTH)

logger = logging_tool.get_logger(__name__)

#pygame.freetype.init()
#MY_FONT = pygame.freetype.SysFont('Arial', 24)

START_GAME = pygame.USEREVENT + 2

class MainMenuScene(pygame.sprite.Sprite):
    _updatable = pygame.sprite.Group()
    _drawable = pygame.sprite.Group()

    def __init__(self):
        logger.info("Initializing Main Menu Scene")

        super().__init__()
        self.running = True
        self.objects = pygame.sprite.Group()
        self.background = None
        
        self._create_objects()

    def _create_objects(self):
        logger.info("Creating Main Menu Scene Objects")

        # Title
        banner_size = int(80/100*SCREEN_WIDTH), 0#int(20/100*SCREEN_HEIGHT)
        banner = Banner("ban_title", "resources/images/title.bmp", SCREEN_WIDTH//2-banner_size[0]//2, int(0/100*SCREEN_HEIGHT), *banner_size)
        
        button_size = int(20/100*SCREEN_WIDTH), int(10/100*SCREEN_HEIGHT)
        # Start Game Button
        start_button = Button("bStartGame", "resources/images/start.bmp", SCREEN_WIDTH//2-button_size[0]//2, int(40/100*SCREEN_HEIGHT), START_GAME, *button_size, (175, 125, 0))
        # Quit Game Button
        quit_button = Button("bQuitGame","resources/images/quit.bmp", SCREEN_WIDTH//2-button_size[0]//2, int(60/100*SCREEN_HEIGHT), pygame.QUIT, *button_size, (175, 125, 0))

        #self.objects.add(banner)
        #self.objects.add(start_button)
        #self.objects.add(quit_button)

        self._updatable.add(start_button, quit_button)
        self._drawable.add(banner, start_button, quit_button)

    def update(self, dt):
        #quit_button = Button("Quit Game", 50, (255, 255, 255), (SCREEN_WIDTH/2, 400))
        if not self.running:
            return
        for object in self._updatable:
            object.update(dt)

    def draw(self, screen):
        if not self.running:
            return
        for object in self._drawable:
            object.draw(screen)

    def deactivate(self):
        self.running = False
