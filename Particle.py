from functools import partial

import numpy as np
from scipy.optimize import minimize

from settings import ALPHA


class Observation:
    def __init__(self, r, m):
        self.r = r
        self.m = m


def prior_preference(r_o, m_o):
    """事前の選好を計算する。
    r_o: 観測された物体の相対位置
    m_o: 観測された物体の質量
    観測された物体の質量が大きいほど、観測者はその物体を近づけるように行動する。
    """
    return m_o * np.linalg.norm(r_o)**2


def expected_free_energy(
        _self: 'Particle',
        obsv: Observation,
        a: np.ndarray):
    """期待自由エネルギーを計算する"""
    # 選好
    preference_term = prior_preference(obsv.r - a, obsv.m)

    # 慣性（前回アクションと同じ場合に小さな値を取る）
    inertia_term = _self.mass * np.linalg.norm(_self.action - a)**2

    return (1 - ALPHA) * preference_term + ALPHA * inertia_term


class Particle:
    def __init__(self, position, v0, mass=1.0):
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
            m_noise = np.random.normal(0, r_norm * noise_std, size=1)

            self.observations[id(other)] = Observation(
                r=r + r_noise,
                m=other.mass + m_noise,
            )

    def choose_action(self):
        total_action = np.zeros(2)
        for observation in self.observations.values():
            partial_efe = partial(
                expected_free_energy,
                self,
                observation)
            res = minimize(partial_efe, [0, 0])
            action = res.x

            total_action += action

        self.action = total_action

    def act(self, dt):
        self.position += self.action * dt
