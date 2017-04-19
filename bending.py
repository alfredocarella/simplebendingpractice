import math
import numpy as np


class Beam():
    def __init__(self, length):
        self.length = length


class DistributedLoad:
    def __init__(self, coeffs, left, right):
        self.y_load = np.poly1d(coeffs)
        self.left = left
        self.right = right
        load_integral = self.y_load.integ()
        y_force = load_integral(self.right) - load_integral(self.left)
        moment_integral = (self.y_load * np.poly1d([1, 0])).integ()
        x_coord = (moment_integral(self.right) - moment_integral(self.left)) / y_force
        self.resultant = PointLoad([0, y_force], x_coord)
        self.moment = self.resultant.moment

    def value_at(self, coord):
        if self.left <= coord <= self.right:
            return self.y_load(coord - self.left)
        else:
            return 0


class PointLoad:
    def __init__(self, vector2d, x_coord):
        self.vector2d = np.array([*vector2d])
        self.x_coord = x_coord
        self.x, self.y = self.vector2d
        self.norm = math.sqrt(sum(comp ** 2 for comp in vector2d))
        self.resultant = self
        self.moment = self.y * x_coord


class PointTorque:
    def __init__(self, torque, x_coord):
        self.x_coord = x_coord
        self.moment = torque
        self.resultant = 0
