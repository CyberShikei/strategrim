#!./.venv/bin/python

import pygame

from src import UnitStack, Unit, RubberBandSelector

from config import SCREEN_HEIGHT, SCREEN_WIDTH, GAME_TITLE

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
    selectables = pygame.sprite.Group()

    # Create the object group
    unit_stacks = pygame.sprite.Group()
    #units = pygame.sprite.Group()
    
    #selector = pygame.sprite.Group()

    # Add objects to the groups
    UnitStack.containers = (unit_stacks, updatable, drawable, selectables)
    #Unit.containers = (units, updatable, drawable)

    #RubberBandSelector.containers = (selectors)

    # Create the player
    init_stack = UnitStack(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 29), UnitStack(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, 20), UnitStack(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, 25)
    unit_stacks.add(init_stack)
    updatable.add(init_stack)
    drawable.add(init_stack)
    selectables.add(init_stack)

    # Create the selector
    selector = RubberBandSelector(color=(255, 255, 255), thickness=2)
    mouse_down = False
    mouse_event = None

    # Start the game loop
    running = True
    while running:
        # check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # On key plress q or esc, quit the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    selector.activate()
                elif event.button == 3:
                    for stack in unit_stacks:
                        stack.move_towards(event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                selector.deactivate()


        # fill the screen with black
        screen.fill((0, 0, 0))

        if selector.isActive():
            selector.update(screen)
            for selectable in selectables:
                if selectable.is_in_area(selector.get_rect_points()):
                    selectable.select()
                else:
                    selectable.deselect()

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
