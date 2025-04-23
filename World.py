
import pygame

from settings import BG_COLOR, COLORS, NOISE_STD
from Particle import Particle


# 座標変換関数
def to_screen_coords(pos, width, height):
    # シミュレーション座標系から画面座標系への変換
    x = width // 2 + pos[0] * (width / 4)
    y = height // 2 - pos[1] * (height / 4)  # y座標は反転
    return (int(x), int(y))


class World:
    def __init__(self, screen: pygame.Surface, particles: list[Particle]):
        self.screen = screen
        self.particles = particles
        self.history = [[] for _ in particles]

    def step(self, dt: float):
        for p in self.particles:
            others = [p_ for p_ in self.particles if id(p) != id(p_)]
            p.observe(others, noise_std=NOISE_STD)

        for p in self.particles:
            p.choose_action()
            p.act(dt)

    def draw(self):
        # 画面のクリア
        self.screen.fill(BG_COLOR)
        for i, p in enumerate(self.particles):
            # 軌跡の描画
            if len(self.history[i]) > 1:
                points = [
                    to_screen_coords(
                        pos,
                        self.screen.get_width(),
                        self.screen.get_height())
                    for pos in self.history[i]]
                pygame.draw.lines(self.screen, COLORS[i], False, points, 1)
            current_pos = to_screen_coords(
                p.position,
                self.screen.get_width(),
                self.screen.get_height())
            self.history[i].append(p.position.copy())

            # 現在位置の描画
            pygame.draw.circle(self.screen, COLORS[i], current_pos, 5)

            # 粒子名の表示
            font = pygame.font.Font(None, 24)
            text = font.render(
                f"(x={p.position[0]:.1f}, y={p.position[1]:.1f})",
                True,
                COLORS[i])
            self.screen.blit(text, (current_pos[0] + 10, current_pos[1] - 10))
