import numpy as np

from constants import G


class Particle:
    def __init__(self, mass, position, velocity, color):
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.acceleration = np.zeros(2)
        self.color = color

    def calculate_force(self, other):
        r = other.position - self.position
        distance = np.linalg.norm(r)
        force_magnitude = G * self.mass * other.mass / (distance ** 2)
        force = force_magnitude * r / distance
        return force
