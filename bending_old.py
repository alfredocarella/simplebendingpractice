import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from sympy import integrate, Piecewise, symbols, lambdify
from sympy.core.sympify import sympify


class Beam:
    def __init__(self, length, fixed_and_rolling_coords):
        x = symbols('x')
        self.length = length
        self.fixed_coord, self.rolling_coord = fixed_and_rolling_coords
        self.load_inventory = []
        self.fixed_support, self.rolling_support = ((0, 0), 0)
        self.distributed_loads = [0, 0]
        self.normal_and_shear_force = [0, 0]
        self.bending_moment = 0
        self.fixed_load = [Piecewise((0, x < self.fixed_coord), (0, x > self.length), (self.fixed_support[0], True)),
                           Piecewise((0, x < self.fixed_coord), (0, x > self.length), (self.fixed_support[1], True))]
        self.rolling_load = [0,
                             Piecewise((0, x < self.rolling_coord), (0, x > self.length), (self.rolling_support, True))]

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
        self.fixed_support, self.rolling_support = tuple(sol[0:-1]), sol[-1]
        x = symbols('x')
        self.fixed_load = [Piecewise((0, x < self.fixed_coord), (0, x > self.length), (self.fixed_support[0], True)),
                           Piecewise((0, x < self.fixed_coord), (0, x > self.length), (self.fixed_support[1], True))]
        self.rolling_load = [0,
                             Piecewise((0, x < self.rolling_coord), (0, x > self.length), (self.rolling_support, True))]

    def update_distributed_loads(self):
        x = symbols('x')
        self.distributed_loads = [0, 0]
        for load in self.load_inventory:
            if type(load).__name__ == "DistributedLoad":
                self.distributed_loads[0] += load.x_load
                self.distributed_loads[1] += load.y_load

    def update_normal_and_shear_forces(self):
        x, t = symbols('x t')
        self.normal_and_shear_force[0] = integrate(self.distributed_loads[0], (x, 0, t)).subs(t, x)
        self.normal_and_shear_force[0] += self.fixed_load[0]

        self.normal_and_shear_force[1] = integrate(self.distributed_loads[1], (x, 0, t)).subs(t, x)
        # self.normal_and_shear_force[1] = integrate(self.distributed_loads[1], (x, 0, x))
        self.normal_and_shear_force[1] += self.fixed_load[1]
        self.normal_and_shear_force[1] += self.rolling_load[1]

        for load in self.load_inventory:
            if type(load).__name__ == "PointLoad":
                self.normal_and_shear_force[0] += Piecewise((0, x < load.x_coord), (0, x > self.length), (load.fx, True))
                self.normal_and_shear_force[1] += Piecewise((0, x < load.x_coord), (0, x > self.length), (load.fy, True))

    def update_bending_moment(self):
        x, t = symbols('x t')
        # FIXME  (x, a, b) <-- setting b (integration limit) to "x" (integration variable) breaks things. Stupid error!
        # self.bending_moment = integrate(self.normal_and_shear_force[1], (x, 0, self.length))
        # self.bending_moment = integrate(self.normal_and_shear_force[1], x).subs(x, 7)
        self.bending_moment = integrate(integrate(self.distributed_loads[1], (x, 0, self.length)), (x, 0, t)).subs(t, x)

        self.bending_moment += Piecewise((0, x < self.fixed_coord), (0, x > self.length), ((x-self.fixed_coord) * self.fixed_support[1], True))
        self.bending_moment += Piecewise((0, x < self.rolling_coord), (0, x > self.length), ((x-self.rolling_coord) * self.rolling_support, True))

        for load in self.load_inventory:
            if type(load).__name__ == "PointLoad":
                self.bending_moment += Piecewise((0, x < load.x_coord), (0, x > self.length), ((x-load.x_coord)*load.fy, True))
            if type(load).__name__ == "PointTorque":
                self.bending_moment += Piecewise((0, x < load.x_coord), (0, x > self.length), (load.moment, True))

    def plot(self, num_points=None):
        if num_points is None:
            num_points = 1000 - 1000 % self.length + 1
        x_axis = np.linspace(0, self.length, num_points)
        try:
            fig, ax = plt.subplots(1, 1, sharex='all', sharey='none')
            plot_analytical(ax, x_axis, self.normal_and_shear_force[0], filename="01_normal", maxmin_hline=True, x_units="m", y_units='kN', ylabel="Normalkraft", facecolor="b")
        except:
            print("OBS! Normalkraftdiagram IKKE generert!")
        try:
            fig, ax = plt.subplots(1, 1, sharex='all', sharey='none')
            plot_analytical(ax, x_axis, self.normal_and_shear_force[1], filename="02_shear", maxmin_hline=True, x_units="m", y_units='kN', ylabel="Skjærkraft", facecolor="r")
        except:
            print("OBS! Skjærkraftdiagram IKKE generert!")
        try:
            fig, ax = plt.subplots(1, 1, sharex='all', sharey='none')
            plot_analytical(ax, x_axis, self.bending_moment, filename="03_bending", maxmin_hline=True, x_units="m", y_units='kN \cdot m', ylabel="Bøyemoment", facecolor="y")
        except:
            print("OBS! Bøyemomentdiagram IKKE generert!")


class DistributedLoad:
    def __init__(self, x_expr, y_expr, span):
        self.span = span
        x = symbols('x')
        x_func = sympify(x_expr).subs(x, x - span[0])
        y_func = sympify(y_expr).subs(x, x - span[0])
        self.x_load = Piecewise((0, x < span[0]), (0, x > span[1]), (x_func, True))
        self.y_load = Piecewise((0, x < span[0]), (0, x > span[1]), (y_func, True))
        x_resultant = integrate(self.x_load, (x, *span))
        y_resultant = integrate(self.y_load, (x, *span))
        coord_resultant = integrate(self.y_load * x, (x, *span)) / y_resultant
        self.resultant = PointLoad((x_resultant, y_resultant), coord_resultant)
        self.moment = self.resultant.moment

    def value_at(self, x_coord):
        return self.x_load.subs("x", x_coord), self.y_load.subs("x", x_coord)


class PointLoad:
    """
    Point load 2D vector applied at a point (counterclockwise positive).
    Consists of a size 2 iterable and an application point 'x_coord'.
    """

    def __init__(self, vector2d, x_coord, beam_length=0):
        x = symbols('x')
        self.beam_length = beam_length
        self.fx, self.fy = vector2d
        self.x_coord = x_coord
        self.resultant = self
        self.moment = self.fy * x_coord
        self.normal_and_shear = [Piecewise((0, x < self.x_coord), (self.fx, True)),
                                 Piecewise((0, x < self.x_coord), (self.fy, True))]


class PointTorque:
    """
    Torque applied at a point (counterclockwise positive). Consists of a
    scalar magnitude and an application point 'x_coord'.
    """

    def __init__(self, torque, x_coord):
        self.x_coord = x_coord
        self.resultant = PointLoad([0, 0], x_coord)
        self.moment = torque


def plot_analytical(ax, x_vec, sym_func, title="", filename="foo", maxmin_hline=False, x_units="m", y_units='kN \cdot m', ylabel="Bøyemoment", facecolor=None):
    x = symbols('x')
    lambda_function = lambdify(x, sym_func)
    y_vec = lambda_function(x_vec)
    return plot_numerical(ax, x_vec, y_vec, title, filename, maxmin_hline, x_units, y_units, ylabel, facecolor)


def plot_numerical(ax, x_vec, y_vec, title="", filename="foo", maxmin_hline=False, x_units="m", y_units='kN \cdot m', ylabel="Bøyemoment", facecolor=None):
    ax.plot(x_vec, y_vec, '0.5', linewidth=2)
    a, b = x_vec[0], x_vec[-1]
    verts = [(a, 0)] + list(zip(x_vec, y_vec)) + [(b, 0)]
    if not facecolor:
        facecolor = '0.9'
    poly = Polygon(verts, facecolor=facecolor, edgecolor='0.5', alpha=0.7)
    ax.add_patch(poly)
    if title:
        ax.set_title(title)
    ax.set_xlim([x_vec.min(), x_vec.max()])
    if maxmin_hline:
        ax.axhline(y=max(y_vec), linestyle='--', color="g")
        max_idx = y_vec.argmax()
        ax.set_xlabel('Bjelkeakse $[{}]$'.format(x_units))
        ax.set_ylabel("{} $[{}]$".format(ylabel, y_units))
        plt.annotate('${:0.2f}'.format(y_vec[max_idx]).rstrip('0').rstrip('.') + " {}$".format(y_units),
                     xy=(x_vec[max_idx], y_vec[max_idx]), xytext=(8, 0), xycoords=('data', 'data'),
                     textcoords='offset points', size=12)
        ax.axhline(y=min(y_vec), linestyle='--', color="g")
        min_idx = y_vec.argmin()
        plt.annotate('${:0.2f}'.format(y_vec[min_idx]).rstrip('0').rstrip('.') + " {}$".format(y_units),
                     xy=(x_vec[min_idx], y_vec[min_idx]), xytext=(8, 0), xycoords=('data', 'data'),
                     textcoords='offset points', size=12)

        plt.savefig('{}.pdf'.format(filename), bbox_inches='tight', rasterized=True)
    return plt
