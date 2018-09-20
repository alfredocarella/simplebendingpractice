from collections import namedtuple
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import sympy

# plt.rc('text', usetex=True)  # This makes it prettier... but also slower


DistributedLoad = namedtuple("DistributedLoad", "expr, span")  # ,shift")
PointLoad = namedtuple("PointLoad", "force, coord")


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


def create_distributed_load(expr: str, interval: tuple=None, shift: bool=True):
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
