import numpy as np


class DistributedLoad:
    def __init__(self, coeffs, left, right):
        self.poly = np.poly1d(coeffs)
        self.left = left
        self.right = right

    def value_at(self, coord):
        if self.left <= coord <= self.right:
            return self.poly(coord - self.left)
        else:
            return 0


class Beam():
    def __init__(self, length):
        self.length = length
