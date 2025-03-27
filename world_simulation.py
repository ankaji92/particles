import pygame
import numpy as np

from Particle import Particle
from constants import (
    SCALE,
    SCREEN_SHAPE,
    SCREEN_CENTER,
    BG_COLOR,
    DELTA_T,
    CIRCLE_RADIUS
)


def init_simulation():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SHAPE)
    pygame.display.set_caption("Three Body Problem")
    clock = pygame.time.Clock()

    # 3つの粒子を初期化（異なる色で）
    particles = [
        Particle(1.0e30, [0, 0], [0, 0], (255, 0, 0)),  # 赤
        Particle(1.0e30, [1.5e11, 0], [0, 3.0e4], (0, 255, 0)),  # 緑
        Particle(1.0e30, [0, 1.5e11], [-3.0e4, 0], (0, 0, 255))  # 青
    ]
    return screen, clock, particles


def update_particles(particles, dt):
    # 各粒子の力を計算
    for i, particle in enumerate(particles):
        total_force = np.zeros(2)
        for j, other in enumerate(particles):
            if i != j:
                total_force += particle.calculate_force(other)

        # 加速度、速度、位置を更新
        particle.acceleration = total_force / particle.mass
        particle.velocity += particle.acceleration * dt
        particle.position += particle.velocity * dt


def draw_particles(screen, particles):
    screen.fill(BG_COLOR)  # 黒背景

    # 各粒子を描画
    for particle in particles:
        screen_pos = particle.position / SCALE + SCREEN_CENTER
        pygame.draw.circle(
            screen,
            particle.color,
            screen_pos,
            CIRCLE_RADIUS
        )

    pygame.display.flip()


def run_simulation():
    screen, clock, particles = init_simulation()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        update_particles(particles, DELTA_T)
        draw_particles(screen, particles)
        clock.tick(60)  # 60FPSに制限

    pygame.quit()


if __name__ == "__main__":
    run_simulation()
