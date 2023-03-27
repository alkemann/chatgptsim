import pygame
import numpy as np
import configparser
from environment import Environment


def main():
    # Read configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')

    environment = Environment(config)

    # Set up Pygame window
    pygame.init()
    pygame.display.set_caption("Evolution Simulation")

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Display environment
        environment.display()


if __name__ == '__main__':
    main()
