import sys

import pygame

from Particle import Particle
from World import World
from settings import WIDTH, HEIGHT, DELTA_T, STEPS


def main():
    # Pygameの初期化
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(
        "Subjective Mass Estimation and Particle Motion"
    )

    # 粒子の初期化（太陽と2つの惑星）
    particles = [
        Particle(
            position=[-0.5, 0.0],
            v0=[0.0, -1.0],
            mass=1.0),
        Particle(
            position=[0.5, 0.0],
            v0=[0.0, 1.0],
            mass=1.0)]

    world = World(screen, particles)

    clock = pygame.time.Clock()
    running = True

    for _ in range(STEPS):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not running:
            break

        world.step(DELTA_T)

        world.draw()

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
