import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from sympy import integrate, Piecewise, symbols, lambdify


def get_reaction_forces(x_coords:tuple, resultant_force:tuple, resultant_moment:float):
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


def plot_analytical(ax, x_vec, sym_func, title="", filename="foo", maxmin_hline=False, x_units="m", y_units='kN \cdot m', ylabel="Bøyemoment", facecolor='0.9'):
    x = symbols('x')
    lambda_function = lambdify(x, sym_func, "numpy")
    x_vec = np.asarray(x_vec)
    y_vec = lambda_function(x_vec)

    ax.plot(x_vec, y_vec, '0.5', linewidth=2)

    # put into function
    a, b = x_vec[0], x_vec[-1]
    verts = [(a, 0)] + list(zip(x_vec, y_vec)) + [(b, 0)]
    poly = Polygon(verts, facecolor=facecolor, edgecolor='0.5', alpha=0.5)
    ax.add_patch(poly)

    # put into own function
    ax.set_xlim([x_vec.min(), x_vec.max()])
    if maxmin_hline:
        ax.axhline(y=max(y_vec), linestyle='--', color="g", alpha=0.5)
        max_idx = y_vec.argmax()
        ax.axhline(y=min(y_vec), linestyle='--', color="g", alpha=0.5)
        min_idx = y_vec.argmin()
        plt.annotate('${:0.1f}'.format(y_vec[max_idx]).rstrip('0').rstrip('.') + " {}$".format(y_units),
                     xy=(x_vec[max_idx], y_vec[max_idx]), xytext=(8, 0), xycoords=('data', 'data'),
                     textcoords='offset points', size=12)
        plt.annotate('${:0.1f}'.format(y_vec[min_idx]).rstrip('0').rstrip('.') + " {}$".format(y_units),
                     xy=(x_vec[min_idx], y_vec[min_idx]), xytext=(8, 0), xycoords=('data', 'data'),
                     textcoords='offset points', size=12)

    # take out of function body
    if title:
        ax.set_title(title)
    ax.set_xlabel('Bjelkeakse $[{}]$'.format(x_units))
    ax.set_ylabel("{} $[{}]$".format(ylabel, y_units))
#        plt.savefig('{}.pdf'.format(filename), bbox_inches='tight', rasterized=True)
    return plt
