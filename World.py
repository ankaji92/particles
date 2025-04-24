from typing import Optional

import numpy as np
import pygame

from settings import BG_COLOR, O_COLOR, P_COLOR, NOISE_STD
from Particle import Particle


# 座標変換関数
def to_screen_coords(pos, width, height, max_distance, offset=0.9):
    # シミュレーション座標系から画面座標系への変換
    x = width // 2 + width / (2 + offset) / max_distance * pos[0]
    y = height // 2 + height / (2 + offset) / max_distance * pos[1]  # y座標は反転
    return (int(x), int(y))


class World:
    def __init__(
            self,
            screen: pygame.Surface,
            particles: list[Particle],
            origin_idx: Optional[int] = None):
        self.screen = screen
        self.particles = particles
        self.history = [[] for _ in particles]
        self.origin_idx = origin_idx
        if origin_idx is None:
            self.origin = np.zeros(2)
        else:
            self.origin = self.particles[origin_idx].position
        self.max_distance = np.max(np.array([
            np.linalg.norm(p.position - self.origin)
            for p in self.particles]))

    def step(self, dt: float):
        for p in self.particles:
            others = [p_ for p_ in self.particles if id(p) != id(p_)]
            p.observe(others, noise_std=NOISE_STD)

        for p in self.particles:
            p.choose_action(dt)
            p.act(dt)

    def draw(self):
        # 画面のクリア
        self.screen.fill(BG_COLOR)

        for i, p in enumerate(self.particles):
            pos_from_origin = p.position - self.origin
            is_origin = i == self.origin_idx
            if not is_origin:
                # 軌跡の描画
                if len(self.history[i]) > 1:
                    points = [
                        to_screen_coords(
                            pos,
                            self.screen.get_width(),
                            self.screen.get_height(),
                            self.max_distance)
                        for pos in self.history[i]]
                    pygame.draw.lines(self.screen, P_COLOR, False, points, 1)

            current_pos = to_screen_coords(
                pos_from_origin,
                self.screen.get_width(),
                self.screen.get_height(),
                self.max_distance)
            self.history[i].append(pos_from_origin)

            # 現在位置の描画
            pygame.draw.circle(
                self.screen,
                O_COLOR if is_origin else P_COLOR,
                current_pos,
                5)

            # 粒子名の表示
            font = pygame.font.Font(None, 24)
            text = font.render(
                f"(x={p.position[0]:.1f}, y={p.position[1]:.1f})",
                True,
                O_COLOR if is_origin else P_COLOR)
            self.screen.blit(text, (current_pos[0] + 10, current_pos[1] - 10))
