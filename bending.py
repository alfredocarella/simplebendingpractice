import math
import numpy as np


class Beam():
    def __init__(self, length):
        self.length = length
        self.load_inventory = []

    def add_load(self, new_load):
        self.load_inventory.append(new_load)


class DistributedLoad:
    def __init__(self, coeffs, x_left, x_right):
        self.y_load = np.poly1d(coeffs)
        self.x_left = x_left
        self.x_right = x_right
        load_integral = self.y_load.integ()
        y_force = load_integral(self.x_right - self.x_left) - load_integral(0)
        moment_integral = (self.y_load * np.poly1d([1, 0])).integ()
        x_coord = (moment_integral(self.x_right - self.x_left) - moment_integral(0)) / y_force + self.x_left
        self.resultant = PointLoad([0, y_force], x_coord)
        self.moment = self.resultant.moment

    def value_at(self, coord):
        if self.x_left <= coord <= self.x_right:
            return self.y_load(coord - self.x_left)
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
