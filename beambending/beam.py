from collections import namedtuple
from contextlib import contextmanager
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
import numpy as np
import os
import sympy
from sympy import integrate

# plt.rc('text', usetex=True)  # This makes the text prettier... and SLOWER


DistributedLoad = namedtuple("DistributedLoad", "expr, span")  # ,shift")
PointLoad = namedtuple("PointLoad", "force, coord")


def plot_and_save(x0, x1, dist_forces, shear_forces, bending_moments):
    """
    TODO: Write a decent docstring

    :param x0:
    :param x1:
    :param dist_forces:
    :param shear_forces:
    :param bending_moments:
    :return:
    """
    fig = plt.figure(figsize=(6, 10))
    fig.subplots_adjust(hspace=0.4)
    x_axis = np.linspace(x0, x1, (x1 - x0) * 1000 + 1)

    # TODO: Take care of beam plotting
    ax1 = fig.add_subplot(4, 1, 1)
    ax1.text(0.6, 0.5, "A plot of the loaded beam is coming.\nGive me one more day!", size=12, rotation=20.,
             ha="center", va="center",
             bbox=dict(boxstyle="round",
                       ec=(1., 0.5, 0.5),
                       fc=(1., 0.8, 0.8),
                       )
             )
    ax1.set_title("Easy examples for beam loading diagrams.")

    ax2 = fig.add_subplot(4, 1, 2)
    plot02_params = {'ylabel': "Distributed loads", 'yunits': r'kN / m',
                     # 'xlabel':"Beam axis", 'xunits':"m",
                     # 'title': r"LATEX TEST $- \frac{2 \sqrt{11}}{5} + \frac{23}{5}$",
                     'color': "b"}
    plot_analytical(ax2, x_axis, sum(dist_forces), **plot02_params)
    ax3 = fig.add_subplot(4, 1, 3)
    plot03_params = {'ylabel': "Shear force", 'yunits': r'kN',
                     # 'xlabel':"Beam axis", 'xunits':"m",
                     'color': "r"}
    plot_analytical(ax3, x_axis, sum(shear_forces), **plot03_params)
    ax4 = fig.add_subplot(4, 1, 4)
    plot04_params = {'ylabel': "Bending moment", 'yunits': r'kN \cdot m',
                     'xlabel': "Beam axis", 'xunits': "m",
                     'color': "y"}
    plot_analytical(ax4, x_axis, sum(bending_moments), **plot04_params)
    plt.savefig(fname="output/test01.pdf")


def plot_analytical(ax:plt.axes, x_vec, sym_func, title:str="", maxmin_hline:bool=True, xunits:str="", yunits:str="", xlabel:str="", ylabel:str="", color=None):
    """
    Dear future me: please write a good docstring as soon as this function is working

    :param ax: a matplotlib.Axes object where the data is to be plotted.
    :param x_vec: array-like, support where the provided symbolic function will be plotted
    :param sym_func: symbolic function using the variable x
    :param title: title to show above the plot, optional
    :param maxmin_hline: when set to False, the extreme values of the function are not displayed
    :param xunits: str, physical unit to be used for the x-axis. Example: "m"
    :param yunits: str, physical unit to be used for the y-axis. Example: "m"
    :param xlabel: str, physical variable displayed on the x-axis. Example: "Length"
    :param ylabel: str, physical variable displayed on the y-axis. Example: "Shear force"
    :param color: color to be used for the shaded area of the plot. No shading if not provided
    :return: a matplotlib.Axes object representing the plotted data.
    """
    x = sympy.symbols('x')
    x_vec = np.asarray(x_vec)
    y_vec = sympy.lambdify(x, sym_func, "numpy")(x_vec)
    ax.plot(x_vec, y_vec, '0.5', linewidth=2)

    if color:
        a, b = x_vec[0], x_vec[-1]
        verts = [(a, 0)] + list(zip(x_vec, y_vec)) + [(b, 0)]
        poly = Polygon(verts, facecolor=color, edgecolor='0.5', alpha=0.5)
        ax.add_patch(poly)

    if maxmin_hline:
        ax.axhline(y=max(y_vec), linestyle='--', color="g", alpha=0.5)
        max_idx = y_vec.argmax()
        ax.axhline(y=min(y_vec), linestyle='--', color="g", alpha=0.5)
        min_idx = y_vec.argmin()
        plt.annotate('${:0.1f}'.format(y_vec[max_idx]).rstrip('0').rstrip('.') + " {}$".format(yunits),
                     xy=(x_vec[max_idx], y_vec[max_idx]), xytext=(8, 0), xycoords=('data', 'data'),
                     textcoords='offset points', size=12)
        plt.annotate('${:0.1f}'.format(y_vec[min_idx]).rstrip('0').rstrip('.') + " {}$".format(yunits),
                     xy=(x_vec[min_idx], y_vec[min_idx]), xytext=(8, 0), xycoords=('data', 'data'),
                     textcoords='offset points', size=12)

    ax.set_xlim([x_vec.min(), x_vec.max()])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    if title:
        ax.set_title(title)

    if xlabel or xunits:
        ax.set_xlabel('{} $[{}]$'.format(xlabel, xunits))

    if ylabel or yunits:
        ax.set_ylabel("{} $[{}]$".format(ylabel, yunits))

    return ax


def calculate_diagrams(beam_span, fixed_support, rolling_support, loads):
    """
    TODO: Write a decent docstring

    :param beam_span:
    :param fixed_support:
    :param rolling_support:
    :param loads:
    :return:
    """
    x = sympy.symbols("x")
    x0, x1 = beam_span
    xA, xB = fixed_support, rolling_support

    F_Rx = 0
    dist_forces = [create_distributed_force(*f) for f in distributed(loads)]
    F_Ry = sum(integrate(load, (x, x0, x1)) for load in dist_forces) + \
           sum(f.force for f in point(loads))
    M_R = sum(integrate(load * x, (x, x0, x1)) for load in dist_forces) + \
          sum(f.force * f.coord for f in point(loads))

    support_coords = xA, xB
    resultant_force = F_Rx, F_Ry
    F_Ax, F_Ay, F_By = get_reaction_forces(support_coords, resultant_force, M_R)

    shear_forces = [integrate(load, (x, x0, x)) for load in dist_forces]
    shear_forces.extend(shear_from_pointload(*f) for f in point(loads))
    shear_forces.append(shear_from_pointload(F_Ay, xA))
    shear_forces.append(shear_from_pointload(F_By, xB))

    bending_moments = [integrate(load, (x, x0, x)) for load in shear_forces]

    return x0, x1, dist_forces, shear_forces, bending_moments


def get_reaction_forces(x_coords: tuple, resultant_force: tuple, resultant_moment: float):
    """
    Calculates the reaction forces for a beam with two supports, given the resulting force applied to the beam.
    The first and second coordinates correspond to a fixed and rolling support respectively.

    :param x_coords: tuple or list with the x-coordinates for each of the two beam supports
    :param resultant_force: tuple with the vector components (Fx, Fy) of the total applied force
    :param resultant_moment: sum of all moments applied to the beam
    :return: F_Ax, F_Ay, F_By: reaction force components for fixed (x,y) and rolling (y) supports
    """
    xA, xB = x_coords
    F_Rx, F_Ry = resultant_force
    M_R = resultant_moment
    A = np.array([[-1, 0, 0],
                  [0, -1, -xA],
                  [0, -1, -xB]]).T
    b = np.array([F_Rx, F_Ry, M_R])
    F_Ax, F_Ay, F_By = np.linalg.inv(A).dot(b)
    return F_Ax, F_Ay, F_By


def create_distributed_force(expr: str, interval: tuple=None, shift: bool=True):
    """
    Create a sympy.Piecewise object representing the provided distributed load.

    :param expr: string with a valid sympy expression.
    :param interval: tuple (x0, x1) containing the extremes of the interval on
     which the load is applied.
    :param shift: when set to False, the x-coordinate in the expression is
     referred to the left end of the beam, instead of the left end of the
     provided interval.
    :return: sympy.Piecewise object with the value of the distributed load.
    """
    x = sympy.symbols("x")
    x0, x1 = interval
    if shift:
        expr = sympy.sympify(expr).subs(x, x - x0)
    return sympy.Piecewise((0, x < x0), (0, x > x1), (expr, True))


def shear_from_pointload(value, coord):
    """
    Create a sympy.Piecewise object representing the shear force caused by a
    point load.

    :param value: float or string with the numerical value of the point load.
    :param coord: x-coordinate on which the point load is applied.
    :return: sympy.Piecewise object with the value of the shear force produced
     by the provided point load.
    """
    x = sympy.symbols("x")
    return sympy.Piecewise((0, x < coord), (value, True))


def distributed(loads:list):
    """
    Filter that only keeps the elements of type DistributedLoad
    :param loads: any iterable
    :return: generator containing only the inputs of type DistributedLoad
    """
    for f in loads:
        if isinstance(f, DistributedLoad):
            yield f


def point(loads:list):
    """
    Filter that only keeps the elements of type PointLoad
    :param loads: any iterable
    :return: generator containing only the inputs of type PointLoad
    """
    for f in loads:
        if isinstance(f, PointLoad):
            yield f


# Here I am beginning with the object oriented version
class Beam:
    def __init__(self, span: tuple=(0, 10)):
        self._x0, self._x1 = span
        self._fixed_support = 2
        self._rolling_support = 8
        self._loads = []
        self._distributed_forces = []
        self._shear_forces = []
        self._bending_moments = []
        self.fixed_support_load = 0
        self.rolling_support_load = 0

    def length(self, length: float):
        if length > 0:
            self._x0 = 0
            self._x1 = length
        else:
            raise ValueError("The provided length must be positive.")

    def fixed_support(self, x_coord: float):
        if self._x0 <= x_coord <= self._x1:
            self._fixed_support = x_coord
        else:
            raise ValueError("The fixed support must be located within the beam span.")

    def rolling_support(self, x_coord: float):
        if self._x0 <= x_coord <= self._x1:
            self._rolling_support = x_coord
        else:
            raise ValueError("The rolling support must be located within the beam span.")

    def point_load(self, force: float, coord: float):
        self._loads.append(PointLoad(force, coord))

    def distributed_load(self, expr: str, span: tuple):
        self._loads.append(DistributedLoad(expr, span))

    def add_loads(self, loads: list):
        for load in loads:
            if isinstance(load, (DistributedLoad, PointLoad)):
                self._loads.append(load)
            else:
                raise TypeError("The provided loads must be of type DistributedLoad or PointLoad")

    def get_reaction_forces(self):
        x = sympy.symbols("x")
        x0, x1 = self._x0, self._x1
        xA, xB = self._fixed_support, self._rolling_support
        F_Rx = 0
        F_Ry = sum(integrate(load, (x, x0, x1)) for load in self._distributed_forces) + \
               sum(f.force for f in self.filter_point_loads())
        M_R = sum(integrate(load * x, (x, x0, x1)) for load in self._distributed_forces) + \
              sum(f.force * f.coord for f in self.filter_point_loads())
        A = np.array([[-1, 0, 0],
                      [0, -1, -xA],
                      [0, -1, -xB]]).T
        b = np.array([F_Rx, F_Ry, M_R])
        F_Ax, F_Ay, F_By = np.linalg.inv(A).dot(b)
        return F_Ax, F_Ay, F_By

    def calculate_loads(self):
        x = sympy.symbols("x")
        x0 = self._x0

        self._distributed_forces = [self.create_distributed_force(f) for f in self.filter_distributed_loads()]

        f_ax, f_ay, f_by = self.get_reaction_forces()
        self.fixed_support_load = PointLoad(f_ay, self._fixed_support)
        self.rolling_support_load = PointLoad(f_by, self._rolling_support)

        self._shear_forces = [integrate(load, (x, x0, x)) for load in self._distributed_forces]
        self._shear_forces.extend(self.shear_from_pointload(f) for f in self.filter_point_loads())
        self._shear_forces.append(self.shear_from_pointload(self.fixed_support_load))
        self._shear_forces.append(self.shear_from_pointload(self.rolling_support_load))

        self._bending_moments = [integrate(load, (x, x0, x)) for load in self._shear_forces]

    def create_distributed_force(self, load: DistributedLoad, shift: bool=True):
        expr, interval = load
        x = sympy.symbols("x")
        x0, x1 = interval
        expr = sympy.sympify(expr)
        if shift:
            expr.subs(x, x - x0)
        return sympy.Piecewise((0, x < x0), (0, x > x1), (expr, True))

    def shear_from_pointload(self, load: PointLoad):
        value, coord = load
        x = sympy.symbols("x")
        return sympy.Piecewise((0, x < coord), (value, True))

    def filter_point_loads(self):
        for f in self._loads:
            if isinstance(f, PointLoad):
                yield f

    def filter_distributed_loads(self):
        for f in self._loads:
            if isinstance(f, DistributedLoad):
                yield f

    def get_distributed_force(self):
        return sum(self._distributed_forces)

    def get_shear_force(self):
        return sum(self._shear_forces)

    def get_bending_moment(self):
        return sum(self._bending_moments)

    def plot_and_save(self):
        fig = plt.figure(figsize=(6, 10))
        fig.subplots_adjust(hspace=0.4)

        # TODO: Take care of beam plotting
        ax1 = fig.add_subplot(3, 1, 1)
        ax1.set_title("Loaded beam example")

        plot01_params = {'ylabel': "Beam loads", 'yunits': r'kN / m',
                         # 'xlabel':"Beam axis", 'xunits':"m",
                         'color': "b",
                         'inverted': True}
        self.plot_analytical(ax1, self.get_distributed_force(), **plot01_params)
        self.draw_beam_schematic(ax1)

        ax2 = fig.add_subplot(3, 1, 2)
        plot02_params = {'ylabel': "Shear force", 'yunits': r'kN',
                         # 'xlabel':"Beam axis", 'xunits':"m",
                         'color': "r"}
        self.plot_analytical(ax2, self.get_shear_force(), **plot02_params)

        ax3 = fig.add_subplot(3, 1, 3)
        plot03_params = {'ylabel': "Bending moment", 'yunits': r'kN \cdot m',
                         'xlabel': "Beam axis", 'xunits': "m",
                         'color': "y"}
        self.plot_analytical(ax3, self.get_bending_moment(), **plot03_params)

        if not os.path.isdir("output"):
            os.makedirs("output")
        plt.savefig(fname="output/test01.pdf")

    def draw_beam_schematic(self, ax):
        # Adjust y-axis
        ymin, ymax = -5, 5
        ylim = (min(ax.get_ylim()[0], ymin), max(ax.get_ylim()[1], ymax))
        ax.set_ylim(ylim)
        yspan = ylim[1] - ylim[0]

        # Draw beam body
        beam_left, beam_right = self._x0, self._x1
        beam_length = beam_right - beam_left
        beam_height = yspan * 0.03
        beam_bottom = -1 * beam_height / 2
        beam_top = beam_bottom + beam_height
        beam_body = Rectangle(
            (beam_left, beam_bottom), beam_length, beam_height, fill=True,
            facecolor="black", clip_on=False
        )
        ax.add_patch(beam_body)

        # Draw arrows at point loads
        for load in (*self.filter_point_loads(),
                     self.fixed_support_load,
                     self.rolling_support_load):
            if load[0] < 0:
                y0, y1 = beam_top, beam_top + yspan * 0.17
            else:
                y0, y1 = beam_bottom, beam_bottom - yspan * 0.17
            ax.annotate("",
                        xy=(load[1], y0), xycoords='data',
                        xytext=(load[1], y1), textcoords='data',
                        arrowprops=dict(arrowstyle="simple", color="blue"),
                        )

        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

    def plot_analytical(self, ax: plt.axes, sym_func, title: str = "", maxmin_hline: bool = True, xunits: str = "",
                        yunits: str = "", xlabel: str = "", ylabel: str = "", color=None, inverted=False):
        x = sympy.symbols('x')
        x_vec = np.linspace(self._x0, self._x1, (self._x1 - self._x0) * 1000 + 1)
        y_vec = sympy.lambdify(x, sym_func, "numpy")(x_vec)
        y_vec *= np.ones(x_vec.shape)

        if inverted:
            y_vec *= -1

        if color:
            a, b = x_vec[0], x_vec[-1]
            verts = [(a, 0)] + list(zip(x_vec, y_vec)) + [(b, 0)]
            poly = Polygon(verts, facecolor=color, edgecolor='0.5', alpha=0.5)
            ax.add_patch(poly)

        if maxmin_hline:
            ax.axhline(y=max(y_vec), linestyle='--', color="g", alpha=0.5)
            max_idx = y_vec.argmax()
            ax.axhline(y=min(y_vec), linestyle='--', color="g", alpha=0.5)
            min_idx = y_vec.argmin()
            plt.annotate('${:0.1f}'.format(y_vec[max_idx]*(1-2*inverted)).rstrip('0').rstrip('.') + " {}$".format(yunits),
                         xy=(x_vec[max_idx], y_vec[max_idx]), xytext=(8, 0), xycoords=('data', 'data'),
                         textcoords='offset points', size=12)
            plt.annotate('${:0.1f}'.format(y_vec[min_idx]*(1-2*inverted)).rstrip('0').rstrip('.') + " {}$".format(yunits),
                         xy=(x_vec[min_idx], y_vec[min_idx]), xytext=(8, 0), xycoords=('data', 'data'),
                         textcoords='offset points', size=12)

        ax.set_xlim([x_vec.min(), x_vec.max()])
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        if title:
            ax.set_title(title)

        if xlabel or xunits:
            ax.set_xlabel('{} $[{}]$'.format(xlabel, xunits))

        if ylabel or yunits:
            ax.set_ylabel("{} $[{}]$".format(ylabel, yunits))

        return ax


@contextmanager
def graphics_output():
    my_beam = Beam()
    x = sympy.symbols("x")

    try:
        yield my_beam, x
        my_beam.calculate_loads()
        my_beam.plot_and_save()
    finally:
        pass