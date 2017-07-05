import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import sympy
from sympy.core.sympify import sympify


class Beam:
    def __init__(self, length, fixed_and_rolling_coords):
        zero = sympify(0)
        self.length = length
        self.fixed_coord, self.rolling_coord = fixed_and_rolling_coords
        self.load_inventory = []
        self.fixed_support, self.rolling_support = ((zero, zero), zero)
        self.distributed_loads = [zero, zero]
        self.normal_and_shear_force = [zero, zero]
        self.bending_moment = zero

    def add_load(self, new_load):
        self.load_inventory.append(new_load)
        self.update_reaction_forces()
        self.update_distributed_loads()
        self.update_normal_and_shear_forces()
        self.update_bending_moment()

    def update_reaction_forces(self):
        d1, d2 = self.fixed_coord, self.rolling_coord
        sum_loads_x = sum(load.resultant.fx for load in self.load_inventory)
        sum_loads_y = sum(load.resultant.fy for load in self.load_inventory)
        sum_moments = sum(load.moment for load in self.load_inventory)
        a_matrix = np.array([[-1, 0, 0],
                             [0, -1, -1],
                             [0, -d1, -d2]])
        b = np.array([sum_loads_x, sum_loads_y, sum_moments])
        sol = np.linalg.inv(a_matrix).dot(b)
        self.fixed_support = tuple(sol[0:-1])
        self.rolling_support = sol[-1]

    def update_distributed_loads(self):
        x = sympy.symbols('x')
        self.distributed_loads = [sympify(0), sympify(0)]
        for load in self.load_inventory:
            if type(load).__name__ == "DistributedLoad":
                # self.distributed_loads[0] += sympy.Piecewise((load.x_load, load.span[0] <= x <= load.span[1]), (0, True))
                self.distributed_loads[0] += load.x_load
                self.distributed_loads[1] += load.y_load

    def update_normal_and_shear_forces(self):
        x = sympy.symbols('x')
        self.normal_and_shear_force[0] = sympy.integrate(self.distributed_loads[0], (x, 0, x))
        self.normal_and_shear_force[1] = sympy.integrate(self.distributed_loads[1], (x, 0, x))

        self.normal_and_shear_force[0] += sympy.Piecewise((0, x < self.fixed_coord), (0, x > self.length), (self.fixed_support[0], True))
        self.normal_and_shear_force[1] += sympy.Piecewise((0, x < self.fixed_coord), (0, x > self.length), (self.fixed_support[1], True))
        self.normal_and_shear_force[1] += sympy.Piecewise((0, x < self.rolling_coord), (0, x > self.length), (self.rolling_support, True))

        for load in self.load_inventory:
            if type(load).__name__ == "PointLoad":
                self.normal_and_shear_force[0] += sympy.Piecewise((0, x < load.x_coord), (0, x > self.length), (load.fx, True))
                self.normal_and_shear_force[1] += sympy.Piecewise((0, x < load.x_coord), (0, x > self.length), (load.fy, True))

    def update_bending_moment(self):
        x = sympy.symbols('x')
        # self.bending_moment = sympy.integrate(self.normal_and_shear_force[1], x)
        self.bending_moment = sympy.integrate(sympy.integrate(self.distributed_loads[1], (x, 0, x)), (x, 0, x))

        self.bending_moment += sympy.Piecewise((0, x < self.fixed_coord), (0, x > self.length), ((x-self.fixed_coord) * self.fixed_support[1], True))
        self.bending_moment += sympy.Piecewise((0, x < self.rolling_coord), (0, x > self.length), ((x-self.rolling_coord) * self.rolling_support, True))

        for load in self.load_inventory:
            if type(load).__name__ == "PointLoad":
                self.bending_moment += sympy.Piecewise((0, x < load.x_coord), (0, x > self.length), ((x-load.x_coord)*load.fy, True))
            if type(load).__name__ == "PointTorque":
                self.bending_moment += sympy.Piecewise((0, x < load.x_coord), (0, x > self.length), (load.moment, True))

    def plot(self, num_points=100):
        fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, sharex='all', sharey='none')
        x_axis = np.linspace(0, self.length, num_points)
        plot_analytical(ax1, x_axis, self.distributed_loads[0], "Distributed loads (x)")
        plot_analytical(ax2, x_axis, self.distributed_loads[1], "Distributed loads (y)")
        plot_analytical(ax3, x_axis, self.normal_and_shear_force[0], "Normal force (x)")
        plot_analytical(ax4, x_axis, self.normal_and_shear_force[1], "Shear force (y)")
        # plot_analytical(ax5, x_axis, beam.normal_and_shear_force[0], "Normal force (x)")
        plot_analytical(ax6, x_axis, self.bending_moment, "Bending moment (y)")
        plt.show()


class DistributedLoad:
    def __init__(self, x_expr, y_expr, span):
        self.span = span
        x = sympy.symbols('x')
        x_func = sympify(x_expr).subs(x, x - span[0])
        y_func = sympify(y_expr).subs(x, x - span[0])
        self.x_load = sympy.Piecewise((0, x < span[0]), (0, x > span[1]), (x_func, True))
        self.y_load = sympy.Piecewise((0, x < span[0]), (0, x > span[1]), (y_func, True))
        x_resultant = sympy.integrate(self.x_load, (x, *span))
        y_resultant = sympy.integrate(self.y_load, (x, *span))
        # coord_resultant = sympy.integrate(self.y_load * (x - span[0]), (x, *span)) / y_resultant + span[0]
        coord_resultant = sympy.integrate(self.y_load * x, (x, *span)) / y_resultant
        self.resultant = PointLoad((x_resultant, y_resultant), coord_resultant)
        self.moment = self.resultant.moment

    def value_at(self, x_coord):
        return self.x_load.subs("x", x_coord), self.y_load.subs("x", x_coord)


class PointLoad:
    """
    Point load 2D vector applied at a point (counterclockwise positive).
    Consists of a size 2 iterable and an application point 'x_coord'.
    """

    def __init__(self, vector2d, x_coord):
        self.fx, self.fy = vector2d
        self.x_coord = x_coord
        self.resultant = self
        self.moment = self.fy * x_coord


class PointTorque:
    """
    Torque applied at a point (counterclockwise positive). Consists of a
    scalar magnitude and an application point 'x_coord'.
    """

    def __init__(self, torque, x_coord):
        self.x_coord = x_coord
        self.resultant = PointLoad([0, 0], x_coord)
        self.moment = torque


def plot_analytical(ax, x_vec, sym_func, title):
    x = sympy.symbols('x')
    lambda_function = sympy.lambdify(x, sym_func)
    y_vec = lambda_function(x_vec)
    return plot_numerical(ax, x_vec, y_vec, title)


def plot_numerical(ax, x_vec, y_vec, title):
    ax.plot(x_vec, y_vec, 'r', linewidth=2)
    a, b = x_vec[0], x_vec[-1]
    verts = [(a, 0)] + list(zip(x_vec, y_vec)) + [(b, 0)]
    poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
    ax.add_patch(poly)
    ax.set_title(title)
    return plt


def my_heaviside(x_values):
    return (x_values >= 0) * 1.0


def my_diracdelta(x_values, *args):
    return x_values * 0
