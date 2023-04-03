import pygame
import configparser
from environment import Environment
from creatures import generate_creatures


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    environment = Environment(config)
    creatures = generate_creatures(config, environment.cell_list)
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        for creature in creatures:
            creature.update(environment.cell_list)
            
        environment.display(screen, font)
        
        
        for creature in creatures:
            creature.render(screen, environment.cell_size)

        pygame.display.flip()
        clock.tick(int(config['world']['fps']))
    pygame.quit()


if __name__ == '__main__':
    main()
