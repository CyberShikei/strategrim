#!./.venv/bin/python

import pygame

from src import MainMenuScene, BattleScene

from config import SCREEN_HEIGHT, SCREEN_WIDTH, GAME_TITLE

# User Event
MAIN_MENU = pygame.USEREVENT + 1
START_GAME = pygame.USEREVENT + 2

def main():
    print(f"Welcome to {GAME_TITLE}!\n")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # initialize the pygame library
    pygame.init()
    
    # create a window with the specified dimensions
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # set the title of the window
    pygame.display.set_caption(GAME_TITLE)

    # clock to control the frame rate
    clock = pygame.time.Clock()
    dt = 0

    # Create updateable and drawable groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    
    #MainMenuScene.containers = (scenes, drawable)

    # Create the main menu scene
    active_scene = MainMenuScene()

    updatable.add(active_scene)
    drawable.add(active_scene)
    
    print(f"Active scene: {active_scene}, Updatable: {updatable}, Drawable: {drawable}")

    # Start the game loop
    running = True
    while running:
        # check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting game")
                running = False
            # On key plress q or esc, quit the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    print("Quitting game")
                    running = False

            elif event.type == MAIN_MENU:
                print("Returning to main menu")
                active_scene.deactivate()
                updatable.remove(active_scene)
                drawable.remove(active_scene)

                active_scene = MainMenuScene()
                updatable.add(active_scene)
                drawable.add(active_scene)
                print(f"Active scene: {active_scene}, Updatable: {updatable}, Drawable: {drawable}")
            elif event.type == START_GAME:
                print("Starting game")
                active_scene.deactivate()
                updatable.remove(active_scene)
                drawable.remove(active_scene)
                
                active_scene = BattleScene()
                updatable.add(active_scene)
                drawable.add(active_scene)
                print(f"Active scene: {active_scene}, Updatable: {updatable}, Drawable: {drawable}")

        # fill the screen with black
        screen.fill((0, 0, 0))

        # update
        for updatable_sprite in updatable:
            updatable_sprite.update(dt)

        # draw
        for drawable_sprite in drawable:
            drawable_sprite.draw(screen)

        # update the display
        pygame.display.flip()
        dt = clock.tick(60) / 1000


main()
