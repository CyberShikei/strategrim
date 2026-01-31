import pygame

from .units import UnitStack
from .rubberbandSelector import RubberBandSelector
from .utils import Banner, Button, logging_tool
from .admiral import Admiral

from config import (SCREEN_WIDTH, SCREEN_HEIGHT)

logger = logging_tool.get_logger(__name__)

MAIN_MENU = pygame.USEREVENT + 1

_button_padding = 1

class BattleScene(pygame.sprite.Sprite):
    def __init__(self):
        logger.info("Initializing Battle Scene")

        super().__init__()
        self.running = True
        self.background = None

        self._updatable = pygame.sprite.Group()
        self._drawable = pygame.sprite.Group()
       
        self._player_name = "player1"
        self._client_player = Admiral(
                self._player_name,
                5,
                (175, 0, 175),
                spawn_point=(0, SCREEN_HEIGHT - int(40/100*SCREEN_HEIGHT))
                )
        self._players = pygame.sprite.Group()

        self._unit_action_buttons = pygame.sprite.Group()

        self._create_ui()
        self._players.add(self._client_player)
        self._create_other_players(self._player_name)

        self._updatable.add(self._players)
        self._drawable.add(self._players)
    
    def _create_ui(self):
        logger.info("Creating Battle Scene UI")
        # Menu Buttoni
        spacing = _button_padding
        button_size = int((3*spacing)/100*SCREEN_WIDTH), int((3*spacing)/100*SCREEN_WIDTH)
        b_menu_pos = int(SCREEN_WIDTH - (button_size[0] + (1*spacing)/100*SCREEN_WIDTH)), int((1*spacing)/100*SCREEN_WIDTH)
        b_menu = Button(#"bMenu", "menu", *b_menu_pos, MAIN_MENU, *button_size, (175, 125, 0))
                active=True,
                py_event=True,
                x=b_menu_pos[0],
                y=b_menu_pos[1],
                width=button_size[0],
                height=button_size[1],
                button_id="bMenu",
                image_path="menu",
                trigger_event=MAIN_MENU)
                

        # Spawn Unit Button
        #b_spawn_unit_pos = int(SCREEN_WIDTH - (button_size[0] + (1*spacing)/100*SCREEN_WIDTH)), int((((1*spacing)/100*SCREEN_WIDTH)) + 50)
        #b_spawn_unit = Button("bSpawnUnit", "resources/images/spawn.bmp", *b_spawn_unit_pos, self.spawn_unit, *button_size, (175, 125, 0), py_event=False)
        
        self._create_unit_action_bar()

        self._updatable.add(b_menu)#, b_spawn_unit)
        self._drawable.add(b_menu)#, b_spawn_unit)
    
    def _create_unit_action_bar(self):
        logger.info("Creating Unit Action Bar")
        # Unit Action Bar
        
        width_perc, height_perc = 100, 10
        ban_bar_size = int(width_perc/100*SCREEN_WIDTH), int(height_perc/100*SCREEN_HEIGHT)
        ban_bar_pos = 0, SCREEN_HEIGHT - ban_bar_size[1]
        ban_unit_action_bar = Banner("banUnitActionBar", "action_bar", *ban_bar_pos, *ban_bar_size)
        
        # Unit Action Buttons
        spacing = int(_button_padding/100*SCREEN_WIDTH)
        button_square = int((3*spacing))
        button_size = button_square, button_square
        b_toggle_stack_density = Button(
                active=False,
                toggle=True,
                toggle_state=True,
                py_event=False,
                x=spacing,
                y=ban_bar_pos[1] + (button_size[1]//2),
                width=button_size[0],
                height=button_size[1],
                background_color=(175, 125, 0),
                button_id="stack_formation0",
                image_path="stack_formation0",
                trigger_event=self._set_stack_unit_density
                )
        
        b_toggle_fire_at_will = Button(
                active=False,
                toggle=True,
                py_event=False,
                x=spacing*2 + button_size[0],
                y=ban_bar_pos[1] + (button_size[1]//2),
                width=button_size[0],
                height=button_size[1],
                background_color=(175, 125, 0),
                button_id="fire_at_will0",
                image_path="fire_at_will0",
                trigger_event=self._toggle_fire_at_will
                )

        self._unit_action_buttons.add(b_toggle_stack_density, b_toggle_fire_at_will)

        self._updatable.add(self._unit_action_buttons)
        self._drawable.add(ban_unit_action_bar, self._unit_action_buttons)
    
    def _create_other_players(self, player_name: String, player_color: tuple = (255, 255, 255)):
        self._players.add(Admiral("player2", 5, (255, 0, 0), spawn_point=(0, int(10/100*SCREEN_HEIGHT))))

    def _activate_unit_action_buttons(self):
        for button in self._unit_action_buttons:
            button.activate()

    def _deactivate_unit_action_buttons(self):
        for button in self._unit_action_buttons:
            button.deactivate()
    
    def check_fire_at_will(self):
        if self._client_player.is_selected():
            for button in self._unit_action_buttons:
                if button.get_id() == "bToggleFireAtWill":
                    if not (button.is_toggled() == self._client_player.has_selected_fire_at_will()):
                        button.toggle_state()

    def check_stack_unit_density(self):
        if self._client_player.is_selected():
            for button in self._unit_action_buttons:
                if button.get_id() == "bToggleStackDensity":
                    if not (button.is_toggled() == self._client_player.has_selected_stack_unit_density()):
                        button.toggle_state()
    
    def button_state_check(self):
        self.check_fire_at_will()
        self.check_stack_unit_density()

    def _set_stack_unit_density(self, state=False):
        self._client_player.set_stack_unit_density(state)

    def _toggle_fire_at_will(self, state=False):

        self._client_player.set_fire_at_will(state)
        #self.check_fire_at_will()
    
    def unit_combat_check(self):
        for player in self._players:
            if player.get_name() != self._client_player.get_name():
                return player.has_range_on_enemy(self._client_player)

    def update(self, dt):
        if not self.running:
            return

        #for event in pygame.event.get():
        #    if event.type == UNITS_SELECTED:
        #        self.check_fire_at_will()

        for button in self._unit_action_buttons:
            if self._client_player.is_selected():
                button.activate()
                self.button_state_check()
            else:
                button.deactivate()
        
        self.unit_combat_check()

        #for event in pygame.event.get():
        #    if event.type == UNITS_SELECTED:
        #        self.check_fire_at_will()

        for object in self._updatable:
            object.update(dt)

    def draw(self, screen):
        if not self.running:
            return

        for object in self._drawable:
            object.draw(screen)
        
    def deactivate(self):
        self.running = False

    def is_left_mouse_down(self):
        if pygame.mouse.get_pressed()[0]:
            self._selector.activate()
        elif not pygame.mouse.get_pressed()[0]:
            self._selector.deactivate()
