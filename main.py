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
    cell_size = int(config['world']['cell_size'])
    screen_width = int(config['world']['width']) * cell_size
    screen_height = int(config['world']['height']) * cell_size
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 18)
    font = pygame.font.SysFont('Arial', 16)
    running = True
    show_stats = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    show_stats = not show_stats
        for creature in creatures:
            creature.update(environment.cell_list, creatures)

        environment.display(screen, font)

        for creature in creatures:
            creature.render(screen, environment.cell_size)
            if show_stats:
                stats_str = f"T:{creature.thirst}/{creature.thirst_threshold} H:{creature.hunger}/{creature.hunger_threshold} S: {creature.stamina}/{creature.stamina_threshold}"
                stats_text = font.render(stats_str, True, (40, 40, 40))
                screen.blit(stats_text, (creature.x * cell_size + 10, creature.y * cell_size + 10))

        pygame.display.flip()
        clock.tick(int(config['world']['fps']))
    pygame.quit()


if __name__ == '__main__':
    main()
