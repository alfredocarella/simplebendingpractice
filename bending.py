import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import math
import numpy as np


class Beam:
    def __init__(self, length, fixed_and_rolling_support_coords, plot_resolution=1000):
        self.length = length
        self.fixed_coord, self.rolling_coord = fixed_and_rolling_support_coords
        self.load_inventory = []
        self.fixed_load, self.rolling_load = (0, 0)
        self.plot_resolution = plot_resolution
        self.distributed_loads = np.zeros(shape=(2, self.plot_resolution))
        self.distributed_loads[0] = np.linspace(0, self.length, self.plot_resolution)

    def add_load(self, new_load):
        self.load_inventory.append(new_load)
        self.update_reaction_forces()
        if type(new_load).__name__ == "DistributedLoad":
            self.update_distributed_loads()

    def update_reaction_forces(self):
        d1, d2 = self.fixed_coord, self.rolling_coord
        sum_loads = sum(load.resultant.y for load in self.load_inventory)
        sum_moments = sum(load.moment for load in self.load_inventory)
        A = np.array([[1, 1],
                      [d1, d2]])
        b = np.array([-1 * sum_loads, -1 * sum_moments])
        self.fixed_load, self.rolling_load = np.linalg.inv(A).dot(b)

    def update_distributed_loads(self):
        new_distributed_loads = np.zeros(shape=(1, self.plot_resolution))
        for load in self.load_inventory:
            if type(load).__name__ == "DistributedLoad":
                new_distributed_loads += load.value_at(self.distributed_loads[0])
        self.distributed_loads[1] = new_distributed_loads

    def plot_numerical(self, xy_array):
        fig, ax = plt.subplots()
        plt.plot(xy_array[0], xy_array[1], 'r', linewidth=2)
        a, b = xy_array[0, 0], xy_array[0, -1]
        verts = [(a, 0)] + list(zip(xy_array[0], xy_array[1])) + [(b, 0)]
        poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
        ax.add_patch(poly)
        return plt


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

    def value_at(self, x_range):
        values = np.zeros((len(x_range)))
        for idx, coord in enumerate(x_range):
            if self.x_left <= coord <= self.x_right:
                values[idx] =self.y_load(coord - self.x_left)
        return values


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
        self.resultant = PointLoad([0, 0], x_coord)
        self.moment = torque
