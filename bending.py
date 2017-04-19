import math
import numpy as np


class Beam():
    def __init__(self, length):
        self.length = length


class DistributedLoad:
    def __init__(self, coeffs, left, right):
        self.poly = np.poly1d(coeffs)
        self.left = left
        self.right = right
        integral = self.poly.integ()
        yval = integral(self.right) - integral(self.left)
        integral2 = (self.poly * np.poly1d([1, 0])).integ()
        x_coord = (integral2(self.right) - integral2(self.left)) / yval
        self.resultant = PointLoad([0, yval], x_coord)

    def value_at(self, coord):
        if self.left <= coord <= self.right:
            return self.poly(coord - self.left)
        else:
            return 0


class PointLoad:
    def __init__(self, vector2d, x_coord):
        self.vector2d = np.array([*vector2d])
        self.x_coord = x_coord
        self.x, self.y = self.vector2d
        self.norm = math.sqrt(sum(comp ** 2 for comp in vector2d))
