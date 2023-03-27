import pygame
import numpy as np
import configparser
from environment import Environment


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    environment = Environment(config)
    pygame.init()
    pygame.display.set_caption("Evolution Simulation")
    screen_width = int(config['world']['width']) * int(config['cell']['size'])
    screen_height = int(config['world']['height']) * int(config['cell']['size'])
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 18)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        environment.display(screen, font)
        pygame.display.flip()
        clock.tick(1)


if __name__ == '__main__':
    main()
