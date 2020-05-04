# Import
import pygame
from pygame.locals import *

# Initialization
pygame.init()

# Display
size_x = 800
size_y = 480
size = (size_x, size_y)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('E-Paper Emulator v 0.1')


def start():
    # Program escape variable
    keepGoing = True
    # New clock
    clock = pygame.time.Clock()
    # Initialize update loop
    pygame.time.set_timer(USEREVENT, 200)
    # Loop
    while keepGoing:
        # Timer
        clock.tick(60)

        # Events
        for event in pygame.event.get():
            # Exit the program
            if event.type == QUIT:
                keepGoing = False
                break

        # Refresh
        update()
        pygame.display.flip()

        # Update Screen
        screen.blit(bg, (0, 0))

        # Redisplay


def update():
    global bg;
    bg = pygame.image.load('output.png')
    bg = pygame.transform.scale(bg, (size))


def stop():
    pass


if __name__ == '__main__':
    update()
    start()
