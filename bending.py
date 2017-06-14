import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import math
import numpy as np
import scipy.integrate
import sympy
from sympy.functions.special.delta_functions import DiracDelta, Heaviside


class Beam:
    def __init__(self, length, fixed_and_rolling_support_coords, plot_resolution=1000):
        self.length = length
        self.fixed_coord, self.rolling_coord = fixed_and_rolling_support_coords
        self.load_inventory = []
        self.fixed_support, self.rolling_support = ((0, 0), 0)
        self.plot_resolution = plot_resolution
        self.x_axis = np.linspace(0, self.length, self.plot_resolution)
        self.distributed_loads = np.zeros((2, self.plot_resolution))
        self.shear_force = np.zeros(self.plot_resolution)
        self.normal_force = np.zeros(self.plot_resolution)
        self.bending_moment = np.zeros(self.plot_resolution)
        self.distributed_loads_analytical = [0, 0]

    def add_load(self, new_load):
        self.load_inventory.append(new_load)
        self.update_reaction_forces()
        # if type(new_load).__name__ == "DistributedLoad":
        self.update_distributed_loads()
        self.update_shear_force()
        self.update_normal_force()
        self.update_bending_moment()

    def update_reaction_forces(self):
        d1, d2 = self.fixed_coord, self.rolling_coord
        sum_loads_x = sum(load.resultant.x for load in self.load_inventory)
        sum_loads_y = sum(load.resultant.y for load in self.load_inventory)
        sum_moments = sum(load.moment for load in self.load_inventory)
        a_matrix = np.array([[-1, 0, 0],
                             [0, -1, -1],
                             [0, -d1, -d2]])
        b = np.array([sum_loads_x, sum_loads_y, sum_moments])
        x_vec = np.linalg.inv(a_matrix).dot(b)
        self.fixed_support, self.rolling_support = x_vec[0:-1], x_vec[-1]

    def update_distributed_loads(self):
        new_distributed_loads = np.vstack((self.x_axis * 0, self.x_axis * 0))
        for load in self.load_inventory:
            if type(load).__name__ == "DistributedLoad":
                new_distributed_loads += load.value_at(self.x_axis)
        self.distributed_loads = new_distributed_loads

        x = sympy.symbols('x')
        self.distributed_loads_analytical = [0, 0]
        for load in self.load_inventory:
            if type(load).__name__ == "DistributedLoad":
                self.distributed_loads_analytical[0] += load.x_load
                self.distributed_loads_analytical[1] += load.y_load
            if type(load).__name__ == "PointLoad":
                self.distributed_loads_analytical[0] += load.vector2d[0] * DiracDelta(x-load.x_coord)
                self.distributed_loads_analytical[1] += load.vector2d[1] * DiracDelta(x-load.x_coord)
        self.distributed_loads_analytical[0] += self.fixed_support[0] * DiracDelta(x-self.fixed_coord)
        self.distributed_loads_analytical[1] += self.fixed_support[1] * DiracDelta(x-self.fixed_coord)
        self.distributed_loads_analytical[1] += self.rolling_support * DiracDelta(x-self.rolling_coord)

    def update_shear_force(self):
        fx, fy = self.distributed_loads
        new_shear_force = np.concatenate(([0], scipy.integrate.cumtrapz(fy, self.x_axis)))

        for idx, coord in enumerate(self.x_axis):
            if self.fixed_coord <= coord:
                new_shear_force[idx] += self.fixed_support[1]
            if self.rolling_coord <= coord:
                new_shear_force[idx] += self.rolling_support

        for load in self.load_inventory:
            if type(load).__name__ == "PointLoad":
                for idx, coord in enumerate(self.x_axis):
                    if load.x_coord <= coord:
                        new_shear_force[idx] += load.resultant.y

        self.shear_force = new_shear_force

        x = sympy.symbols('x')
        fx_analytical = self.distributed_loads_analytical[0]
        fy_analytical = self.distributed_loads_analytical[1]
        self.shear_force_analytical = [0, 0]
        self.shear_force_analytical[0] += sympy.integrate(fx_analytical, x)
        self.shear_force_analytical[1] += sympy.integrate(fy_analytical, x)

    def update_normal_force(self):
        fx, fy = self.distributed_loads
        new_normal_force = np.concatenate(([0], scipy.integrate.cumtrapz(-fx, self.x_axis)))

        for idx, coord in enumerate(self.x_axis):
            if self.fixed_coord <= coord:
                new_normal_force[idx] -= self.fixed_support[0]

        for load in self.load_inventory:
            if type(load).__name__ == "PointLoad":
                for idx, coord in enumerate(self.x_axis):
                    if load.x_coord <= coord:
                        new_normal_force[idx] -= load.resultant.x

        self.normal_force = new_normal_force

    def update_bending_moment(self):
        y = self.shear_force
        new_bending_moment = np.concatenate(([0], scipy.integrate.cumtrapz(y, self.x_axis)))
        for load in self.load_inventory:
            if type(load).__name__ == "PointTorque":
                for idx, coord in enumerate(self.x_axis):
                    if load.x_coord <= coord:
                        new_bending_moment[idx] -= load.moment
        self.bending_moment = new_bending_moment

    def plot_case_this_is_exploratory_coding(self):
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, sharex='all', sharey='none')
        ax1.text(self.length / 2,  # x coordinate, 0 leftmost positioned, 1 rightmost
                 0.5,  # y coordinate, 0 topmost positioned, 1 bottommost
                 "To do: Sketch with reaction forces",  # the text which will be printed
                 horizontalalignment='center',  # shortcut 'ha'
                 verticalalignment='center',  # shortcut 'va'
                 fontsize=20,  # can be named 'font' as well
                 alpha=.5  # float (0.0 transparent through 1.0 opaque)
                 )
        plot_numerical(ax2, (self.x_axis, self.normal_force), "Normal force diagram")
        plot_numerical(ax3, (self.x_axis, self.distributed_loads[1]), "Distributed loads diagram")
        plot_numerical(ax4, (self.x_axis, self.shear_force), "Shear force diagram")
        plot_numerical(ax5, (self.x_axis, self.bending_moment), "Bending moment diagram")
        plt.show()

        x = sympy.symbols('x')
        my_modules = ['numpy', {'Heaviside': my_heaviside, 'DiracDelta': my_diracdelta}]
        y_func = sympy.lambdify(x, self.shear_force_analytical[1], modules=my_modules)
        x_vals = np.linspace(0, self.length, self.plot_resolution)
        y_vals = y_func(x_vals)
        plt.plot(x_vals, y_vals)
        plt.show()


def plot_numerical(ax, xy_array, title):
    ax.plot(xy_array[0], xy_array[1], 'r', linewidth=2)
    a, b = xy_array[0][0], xy_array[0][-1]
    verts = [(a, 0)] + list(zip(xy_array[0], xy_array[1])) + [(b, 0)]
    poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
    ax.add_patch(poly)
    ax.set_title(title)
    return plt


class DistributedLoad:
    def __init__(self, coeffs, span):
        x = sympy.symbols('x')
        x_expr = sum(n * ((x - span[0]) ** p) for p, n in enumerate(coeffs[0][::-1]))
        y_expr = sum(n * ((x - span[0]) ** p) for p, n in enumerate(coeffs[1][::-1]))
        self.x_load = sympy.Piecewise((0, x < span[0]), (0, x > span[1]), (x_expr, True))
        self.y_load = sympy.Piecewise((0, x < span[0]), (0, x > span[1]), (y_expr, True))
        x_force = sympy.integrate(self.x_load, (x, *span))
        y_force = sympy.integrate(self.y_load, (x, *span))
        x_coord_resultant = sympy.integrate(self.y_load * (x - span[0]), (x, *span)) / y_force + span[0]
        self.resultant = PointLoad((x_force, y_force), x_coord_resultant)
        self.moment = self.resultant.moment

    def value_at(self, x_range):
        x = sympy.symbols('x')
        my_modules = ['numpy', {'Heaviside': my_heaviside, 'DiracDelta': my_diracdelta}]
        lam_x_load = sympy.lambdify(x, self.x_load, modules=my_modules)
        lam_y_load = sympy.lambdify(x, self.y_load, modules=my_modules)
        values = np.zeros((2, len(x_range)))
        for idx, coord in enumerate(x_range):
            values[:, idx] = (lam_x_load(coord), lam_y_load(coord))
        return values


class PointLoad:
    """
    Point load 2D vector applied at a point (counterclockwise positive). 
    Consists of a size 2 iterable and an application point 'x_coord'.
    """

    def __init__(self, vector2d, x_coord):
        self.vector2d = np.array([*vector2d])
        self.x_coord = x_coord
        self.x, self.y = self.vector2d
        self.norm = math.sqrt(sum(dim ** 2 for dim in vector2d))
        self.resultant = self
        self.moment = self.y * x_coord


class PointTorque:
    """
    Torque applied at a point (counterclockwise positive). Consists of a 
    scalar magnitude and an application point 'x_coord'.
    """

    def __init__(self, torque, x_coord):
        self.x_coord = x_coord
        self.resultant = PointLoad([0, 0], x_coord)
        self.moment = torque


def my_heaviside(x_values):
    return (x_values >= 0) * 1.0


def my_diracdelta(x_values, *args):
    return x_values * 0
