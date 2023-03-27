import pygame
import numpy as np
import configparser
from environment import Environment


def main():
    # Read configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')
    environment = Environment(config)
    pygame.init()
    pygame.display.set_caption("Evolution Simulation")
    screen_width = int(config['world']['width']) * int(config['cell']['size'])
    screen_height = int(config['world']['height']) * int(config['cell']['size'])
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Display environment
        environment.display(screen)


if __name__ == '__main__':
    main()
