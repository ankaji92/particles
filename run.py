import sys

import pygame

from Particle import Particle
from constants import BLACK, COLORS


# 座標変換関数
def to_screen_coords(pos, width, height):
    # シミュレーション座標系から画面座標系への変換
    scale = 200  # スケールファクター
    x = width // 2 + pos[0] * scale
    y = height // 2 - pos[1] * scale  # y座標は反転
    return (int(x), int(y))


class World:
    def __init__(self, screen: pygame.Surface, particles: list[Particle]):
        self.screen = screen
        self.particles = particles

    def step(self, dt: float):
        for p in self.particles:
            others = [p_ for p_ in self.particles if p.name != p_.name]
            p.observe(others)

        for p in self.particles:
            p.choose_action()
            p.act(dt)

    def draw(self):
        # 画面のクリア
        self.screen.fill(BLACK)
        for p in self.particles:
            # 軌跡の描画
            history = p.get_history()
            if len(history) > 1:
                points = [to_screen_coords(pos, self.screen.get_width(), self.screen.get_height()) for pos in history]
                pygame.draw.lines(self.screen, COLORS[p.name], False, points, 1)

            # 現在位置の描画
            current_pos = to_screen_coords(p.position, self.screen.get_width(), self.screen.get_height())
            pygame.draw.circle(self.screen, COLORS[p.name], current_pos, 5)
            
            # 粒子名の表示
            font = pygame.font.Font(None, 24)
            text = font.render(f"{p.name} (x={p.position[0]:.1f}, y={p.position[1]:.1f})", True, COLORS[p.name])
            self.screen.blit(text, (current_pos[0] + 10, current_pos[1] - 10))


def main():
    # 画面の設定
    WIDTH, HEIGHT = 800, 800

    # Pygameの初期化
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Subjective Mass Estimation and Particle Motion")

    # シミュレーションパラメータ
    dt = 0.1
    steps = 300

    # 粒子の初期化（太陽と2つの惑星）
    planet_0 = Particle(
        name="A",
        position=[-0.5, 0.0],
        v0=[0.0, -1.0],
        mass=1.0
    )
    planet_1 = Particle(
        name="B",
        position=[0.5, 0.0],
        v0=[0.0, 1.0],
        mass=1.0
    )

    particles = [planet_0, planet_1]
    world = World(screen, particles)
    clock = pygame.time.Clock()
    running = True

    for _ in range(steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not running:
            break

        world.step(dt)

        world.draw()

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
