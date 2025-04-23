from math import sin, cos, sqrt

import numpy as np


def prior_preference(x, x_o, m_o):
    """事前の選好を計算する。
    x: 観測者の位置
    x_o: 観測された物体の位置
    m_o: 観測された物体の質量
    観測された物体の質量が大きいほど、観測者はその物体を近づけるように行動する。
    """
    return m_o * np.linalg.norm(x - x_o)**2


def expected_free_energy(x, m, v, x_o, m_o, a):
    """期待自由エネルギーを計算する"""
    alpha = 0.825
    x_pred = x + a

    # 選好
    preference_term = prior_preference(x_pred, x_o, m_o)
    # 慣性（前回アクションと同じ場合に小さな値を取る）
    inertia_term = m * np.linalg.norm(v - a)**2

    return (1 - alpha) * preference_term + alpha * inertia_term


class Particle:
    def __init__(self, name, position, v0, mass=1.0):
        self.name = name
        self.position = np.array(position, dtype=float)
        self.action = np.array(v0, dtype=float)
        self.mass = mass
        self.history = [self.position.copy()]
        self.observations = {}
        directions = [
            np.array([cos(theta), sin(theta)])
            for theta in np.linspace(0, 2 * np.pi, 36, endpoint=False)
        ]
        scalars = [
            s for s in np.linspace(1, 100, 8)
        ]
        self.actions = [s * d for s in scalars for d in directions]

    def observe(self, others: list['Particle'], noise_std=0.01):
        """観測ノイズを加えて観測する"""
        for other in others:
            pos_noise = np.random.normal(0, noise_std, size=2)
            distance = np.linalg.norm(other.position - self.position)
            mass_noise = np.random.normal(0, sqrt(distance) * noise_std, size=1)

            self.observations[other.name] = {
                "position": other.position + pos_noise,
                "mass": other.mass + mass_noise,
            }

    def choose_action(self):
        total_action = np.zeros(2)
        for observation in self.observations.values():
            x = self.position
            m = self.mass
            v = self.action
            x_o = observation["position"]
            m_o = observation["mass"]
            Gs = [expected_free_energy(x, m, v, x_o, m_o, a) for a in self.actions]

            action = self.actions[np.argmin(Gs)]
            total_action += action

        self.action = total_action

    def act(self, dt):
        self.position += self.action * dt
        self.history.append(self.position.copy())

    def get_history(self):
        return np.array(self.history)
