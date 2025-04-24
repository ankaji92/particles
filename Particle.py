from functools import partial

import numpy as np
from scipy.optimize import minimize

from settings import ALPHA, G


class Observation:
    def __init__(self, r, m):
        self.r = r
        self.m = m


def expected_free_energy(
        _self: 'Particle',
        obsv: Observation,
        dt: float,
        a: np.ndarray):
    """期待自由エネルギーを計算する"""
    # 選好
    preference_term = - _self.mass * obsv.m * G / np.linalg.norm(obsv.r - a * dt)

    # 慣性（前回アクションと同じ場合に小さな値を取る）
    inertia_term = _self.mass * np.linalg.norm(_self.action - a)**2

    return (1 - ALPHA) * preference_term + ALPHA * inertia_term


class Particle:
    def __init__(
            self,
            position: tuple[float, float],  # 位置 (x, y) (m)
            v0: tuple[float, float],  # 初速度 (vx, vy) (m/s)
            mass: float):  # 質量 (kg)
        self.position = np.array(position, dtype=float)
        self.action = np.array(v0, dtype=float)
        self.mass = mass
        self.observations = {}

    def observe(self, others: list['Particle'], noise_std=0.01):
        """観測ノイズを加えて観測する"""
        for other in others:
            # 観測ノイズは距離の平方根に比例する
            r = other.position - self.position
            r_norm = np.linalg.norm(r)
            r_noise = np.random.normal(0, r_norm * noise_std, size=2)
            m_noise = np.random.normal(0, r_norm * noise_std)

            self.observations[id(other)] = Observation(
                r=r + r_noise,
                m=other.mass + m_noise,
            )

    def choose_action(self, dt):
        total_action = np.zeros(2)
        for observation in self.observations.values():
            partial_efe = partial(
                expected_free_energy,
                self,
                observation,
                dt)
            res = minimize(partial_efe, [0, 0])
            action = res.x

            total_action += action

        self.action = total_action

    def act(self, dt):
        self.position += self.action * dt
