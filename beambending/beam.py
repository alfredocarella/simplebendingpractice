"""Main module containing the main class Beam, and auxiliary classes PointLoadH,
PointLoadV, DistributedLoadH, and DistributedLoadV.

Example
-------
>>> my_beam = Beam(9)
>>> my_beam.pinned_support = 2    # x-coordinate of the pinned support
>>> my_beam.rolling_support = 7  # x-coordinate of the rolling support
>>> my_beam.add_loads([PointLoadV(-20, 3)])  # 20 kN downwards, at x=3 m
>>> print("(F_Ax, F_Ay, F_By) =", my_beam.get_reaction_forces())
(F_Ax, F_Ay, F_By) = (0.0, 16.0, 4.0)

"""

from collections import namedtuple
from contextlib import contextmanager
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Polygon, Rectangle, RegularPolygon, Wedge
from matplotlib.collections import PatchCollection
import numpy as np
import os
from sympy import integrate, lambdify, Piecewise, sympify
from sympy.abc import x

# plt.rc('text', usetex=True)  # This makes the plot text prettier... but SLOWER


class PointLoadV(namedtuple("PointLoadV", "force, coord")):
    """Vertical point load described by a tuple of floats: (force, coord).

    Examples
    --------
    >>> external_force = PointLoadV(-30, 3)  # 30 kN downwards at x=3 m
    >>> external_force
    PointLoadV(force=-30, coord=3)
    """


class PointLoadH(namedtuple("PointLoadH", "force, coord")):
    """Horizontal point load described by a tuple of floats: (force, coord).

    Examples
    --------
    >>> external_force = PointLoadH(10, 9)  # 10 kN towards the right at x=9 m
    >>> external_force
    PointLoadH(force=10, coord=9)
    """


class DistributedLoadV(namedtuple("DistributedLoadV", "expr, span")):
    """Distributed vertical load, described by its functional form and application interval.

    Examples
    --------
    >>> snow_load = DistributedLoadV("10*x+5", (0, 2))  # Linearly growing load for 0<x<2 m
    
    """


class DistributedLoadH(namedtuple("DistributedLoadH", "expr, span")):
    """Distributed horizontal load, described by its functional form and application interval.

    Examples
    --------
    >>> wind_load = DistributedLoadH("10*x**2+5", (1, 3))  # Quadratically growing load for 1<y<3
    
    """


class PointTorque(namedtuple("PointTorque", "torque, coord")):
    """Point clockwise torque, described by a tuple of floats: (torque, coord).

    Examples
    --------
    >>> motor_torque = PointTorque(30, 4)  # 30 kN·m (clockwise) torque at x=4 m
    
    """


class Beam:
    """
    Represents a one-dimensional beam that can take axial and tangential loads.
    
    Through the method `add_loads`, a Beam object can accept a list of:
    
    * PointLoad objects, and/or
    * DistributedLoad objects.

    Notes
    -----
    * The Beam class currently supports only statically determined beams with
      (exactly) one pinned and one roller support.
    * The default units package units for length, force and bending moment 
      (torque) are respectively (m, kN, kN·m)

    """
    
    def __init__(self, span: float=10):
        """Initializes a Beam object of a given length.

        Parameters
        ----------
        span : float or int
            Length of the beam span. Must be positive, and the pinned and rolling
            supports can only be placed within this span. The default value is 10.

        """
        self._x0 = 0
        self._x1 = span
        self._pinned_support = 2
        self._rolling_support = 8

        self._loads = []
        self._distributed_forces_x = []
        self._distributed_forces_y = []
        self._normal_forces = []
        self._shear_forces = []
        self._bending_moments = []

    @property
    def length(self):
        """float or int: Length of the beam. Must be positive."""
        return self._x1 - self._x0
        
    @length.setter
    def length(self, length: float):
        if length > 0:
            self._x1 = self._x0 + length
        else:
            raise ValueError("The provided length must be positive.")

    @property
    def pinned_support(self):
        """float or int: x-coordinate of the beam's pinned support. Must be 
        within the beam span."""
        return self._pinned_support

    @pinned_support.setter
    def pinned_support(self, x_coord: float):
        if self._x0 <= x_coord <= self._x1:
            self._pinned_support = x_coord
        else:
            raise ValueError("The pinned support must be located within the beam span.")

    @property
    def rolling_support(self):
        """float or int: x-coordinate of the beam's rolling support. Must be 
        within the beam span."""
        return self._rolling_support

    @rolling_support.setter
    def rolling_support(self, x_coord: float):
        if self._x0 <= x_coord <= self._x1:
            self._rolling_support = x_coord
        else:
            raise ValueError("The rolling support must be located within the beam span.")

    def add_loads(self, loads: list):
        """Apply an arbitrary list of (point- or distributed) loads to the beam.

        Parameters
        ----------
        loads : iterable
            An iterable containing DistributedLoad or PointLoad objects to
            be applied to the Beam object. Note that the load application point
            (or segment) must be within the Beam span.

        """
        for load in loads:
            supported_load_types = (DistributedLoadH, DistributedLoadV, PointLoadH, PointLoadV, PointTorque)
            if isinstance(load, supported_load_types):
                self._loads.append(load)
            else:
                raise TypeError("The provided loads must be one of the supported types: {0}".format(supported_load_types))
        self._update_loads()

    def get_reaction_forces(self):
        """
        Calculates the reaction forces at the supports, given the applied loads.
        
        The first and second values correspond to the horizontal and vertical 
        forces of the pinned support. The third one is the vertical force at the
        rolling support.

        Returns
        -------
        F_Ax, F_Ay, F_By: (float, float, float)
            reaction force components for pinned (x,y) and rolling (y) supports 
            respectively.

        """
        x0, x1 = self._x0, self._x1
        xA, xB = self._pinned_support, self._rolling_support
        F_Rx = sum(integrate(load, (x, x0, x1)) for load in self._distributed_forces_x) + \
               sum(f.force for f in self._point_loads_x())
        F_Ry = sum(integrate(load, (x, x0, x1)) for load in self._distributed_forces_y) + \
               sum(f.force for f in self._point_loads_y())
        M_R = sum(integrate(load * x, (x, x0, x1)) for load in self._distributed_forces_y) + \
              sum(f.force * f.coord for f in self._point_loads_y()) + \
              sum(-1 * f.torque for f in self._point_torques())
        A = np.array([[-1, 0, 0],
                      [0, -1, -xA],
                      [0, -1, -xB]]).T
        b = np.array([F_Rx, F_Ry, M_R])
        F_Ax, F_Ay, F_By = np.linalg.inv(A).dot(b)
        return F_Ax, F_Ay, F_By

    def plot(self):
        """Generates a single figure with 4 plots corresponding respectively to:

        - a schematic of the loaded beam
        - normal force diagram,
        - shear force diagram, and
        - bending moment diagram.

        These plots can be generated separately with dedicated functions.

        Returns
        -------
        figure : `~matplotlib.figure.Figure`
            Returns a handle to a figure with the 3 subplots: Beam schematic, 
            shear force diagram, and bending moment diagram.

        """
        fig = plt.figure(figsize=(6, 10))
        fig.subplots_adjust(hspace=0.4)

        ax1 = fig.add_subplot(4, 1, 1)
        self.plot_beam_diagram(ax1)

        ax2 = fig.add_subplot(4, 1, 2)
        self.plot_normal_force(ax2)

        ax3 = fig.add_subplot(4, 1, 3)
        self.plot_shear_force(ax3)

        ax4 = fig.add_subplot(4, 1, 4)
        self.plot_bending_moment(ax4)

        return fig

    def plot_beam_diagram(self, ax=None):
        """Returns a schematic of the beam and all the loads applied on it.
        """
        plot01_params = {'ylabel': "Beam loads", 'yunits': r'kN / m',
                         # 'xlabel':"Beam axis", 'xunits':"m",
                         'color': "g",
                         'inverted': True}
        if ax is None:
            ax = plt.figure(figsize=(6, 2.5)).add_subplot(1,1,1)
        ax.set_title("Loaded beam diagram")
        self._plot_analytical(ax, sum(self._distributed_forces_y), **plot01_params)
        self._draw_beam_schematic(ax)
        return ax.get_figure()

    def plot_normal_force(self, ax=None):
        """Returns a plot of the normal force as a function of the x-coordinate.
        """
        plot02_params = {'ylabel': "Normal force", 'yunits': r'kN',
                         # 'xlabel':"Beam axis", 'xunits':"m",
                         'color': "b"}
        if ax is None:
            ax = plt.figure(figsize=(6, 2.5)).add_subplot(1,1,1)
        self._plot_analytical(ax, sum(self._normal_forces), **plot02_params)
        return ax.get_figure()

    def plot_shear_force(self, ax=None):
        """Returns a plot of the shear force as a function of the x-coordinate.
        """
        plot03_params = {'ylabel': "Shear force", 'yunits': r'kN',
                         # 'xlabel':"Beam axis", 'xunits':"m",
                         'color': "r"}
        if ax is None:
            ax = plt.figure(figsize=(6, 2.5)).add_subplot(1,1,1)
        self._plot_analytical(ax, -1* sum(self._shear_forces), **plot03_params)
        return ax.get_figure()

    def plot_bending_moment(self, ax=None):
        """Returns a plot of the bending moment as a function of the x-coordinate.
        """
        plot04_params = {'ylabel': "Bending moment", 'yunits': r'kN·m',
                         'xlabel': "Beam axis", 'xunits': "m",
                         'color': "y"}
        if ax is None:
            ax = plt.figure(figsize=(6, 2.5)).add_subplot(1,1,1)
        self._plot_analytical(ax, -1* sum(self._bending_moments), **plot04_params)
        return ax.get_figure()

    def _plot_analytical(self, ax: plt.axes, sym_func, title: str = "", maxmin_hline: bool = True, xunits: str = "",
                        yunits: str = "", xlabel: str = "", ylabel: str = "", color=None, inverted=False):
        """
        Auxiliary function for plotting a sympy.Piecewise analytical function.

        :param ax: a matplotlib.Axes object where the data is to be plotted.
        :param x_vec: array-like, support where the provided symbolic function will be plotted
        :param sym_func: symbolic function using the variable x
        :param title: title to show above the plot, optional
        :param maxmin_hline: when set to False, the extreme values of the function are not displayed
        :param xunits: str, physical unit to be used for the x-axis. Example: "m"
        :param yunits: str, physical unit to be used for the y-axis. Example: "kN"
        :param xlabel: str, physical variable displayed on the x-axis. Example: "Length"
        :param ylabel: str, physical variable displayed on the y-axis. Example: "Shear force"
        :param color: color to be used for the shaded area of the plot. No shading if not provided
        :return: a matplotlib.Axes object representing the plotted data.

        """
        x_vec = np.linspace(self._x0, self._x1, int(min(self.length * 1000 + 1, 1e4)))
        y_lam = lambdify(x, sym_func, "numpy")
        y_vec = np.array([y_lam(t) for t in x_vec])

        if inverted:
            y_vec *= -1

        if color:
            a, b = x_vec[0], x_vec[-1]
            verts = [(a, 0)] + list(zip(x_vec, y_vec)) + [(b, 0)]
            poly = Polygon(verts, facecolor=color, edgecolor='0.5', alpha=0.4)
            ax.add_patch(poly)

        if maxmin_hline:
            tol = 1e-3

            if abs(max(y_vec)) > tol:
                ax.axhline(y=max(y_vec), linestyle='--', color="g", alpha=0.5)
                max_idx = y_vec.argmax()
                plt.annotate('${:0.1f}'.format(y_vec[max_idx]*(1-2*inverted)).rstrip('0').rstrip('.') + " $ {}".format(yunits),
                            xy=(x_vec[max_idx], y_vec[max_idx]), xytext=(8, 0), xycoords=('data', 'data'),
                            textcoords='offset points', size=12)

            if abs(min(y_vec)) > tol:
                ax.axhline(y=min(y_vec), linestyle='--', color="g", alpha=0.5)
                min_idx = y_vec.argmin()
                plt.annotate('${:0.1f}'.format(y_vec[min_idx]*(1-2*inverted)).rstrip('0').rstrip('.') + " $ {}".format(yunits),
                            xy=(x_vec[min_idx], y_vec[min_idx]), xytext=(8, 0), xycoords=('data', 'data'),
                            textcoords='offset points', size=12)

        xspan = x_vec.max() - x_vec.min()
        ax.set_xlim([x_vec.min() - 0.01 * xspan, x_vec.max() + 0.01 * xspan])
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        if title:
            ax.set_title(title)

        if xlabel or xunits:
            ax.set_xlabel('{} [{}]'.format(xlabel, xunits))

        if ylabel or yunits:
            ax.set_ylabel("{} [{}]".format(ylabel, yunits))

        return ax

    def _draw_beam_schematic(self, ax):
        """Auxiliary function for plotting the beam object and its applied loads.
        """
        # Adjust y-axis
        ymin, ymax = -5, 5
        ylim = (min(ax.get_ylim()[0], ymin), max(ax.get_ylim()[1], ymax))
        ax.set_ylim(ylim)
        xspan = ax.get_xlim()[1] - ax.get_xlim()[0]
        yspan = ylim[1] - ylim[0]

        # Draw beam body
        beam_left, beam_right = self._x0, self._x1
        beam_length = beam_right - beam_left
        beam_height = yspan * 0.06
        beam_bottom = -(0.75) * beam_height
        beam_top = beam_bottom + beam_height
        beam_body = Rectangle(
            (beam_left, beam_bottom), beam_length, beam_height, fill=True,
            facecolor="brown", clip_on=False, alpha=0.7
        )
        ax.add_patch(beam_body)

        # Markers at beam supports
        pinned_support = Polygon(np.array([self.pinned_support + 0.01*xspan*np.array((-1, -1, 0, 1, 1)), 
                                           beam_bottom + 0.05*np.array((-1.5, -1,0,-1, -1.5))*yspan]).T)
        rolling_support = [Polygon(np.array([self.rolling_support + 0.01*xspan*np.array((-1, 0, 1)), 
                                            beam_bottom + 0.05*np.array((-1,0,-1))*yspan]).T),
                           Polygon(np.array([self.rolling_support + 0.01*xspan*np.array((-1, -1, 1, 1)), 
                                            beam_bottom + 0.05*np.array((-1.5,-1.25, -1.25, -1.5))*yspan]).T)]

        supports = PatchCollection([pinned_support, *rolling_support], facecolor="black")
        ax.add_collection(supports)

        # Draw arrows at point loads
        arrowprops = dict(arrowstyle="simple", color="darkgreen", shrinkA=0.1, mutation_scale=18)
        for load in self._point_loads_y():
            x0 = x1 = load[1]
            if load[0] < 0:
                y0, y1 = beam_top, beam_top + 0.17 * yspan
            else:
                y0, y1 = beam_bottom, beam_bottom - 0.17 * yspan
            ax.annotate("",
                        xy=(x0, y0), xycoords='data',
                        xytext=(x1, y1), textcoords='data',
                        arrowprops=arrowprops
                        )

        for load in self._point_loads_x():
            x0 = load[1]
            y0 = y1 = (beam_top + beam_bottom) / 2.0
            if load[0] < 0:
                x1 = x0 + xspan * 0.05
            else:
                x1 = x0 - xspan * 0.05
            ax.annotate("",
                        xy=(x0, y0), xycoords='data',
                        xytext=(x1, y1), textcoords='data',
                        arrowprops=arrowprops
                        )
        
        # Draw a round arrow at point torques
        for load in self._point_torques():
            xc = load[1]
            yc = (beam_top + beam_bottom) / 2.0
            width = yspan * 0.17
            height = xspan * 0.05
            arc_len= 180

            if load[0] < 0:
                start_angle = 90
                endX = xc + (height/2)*np.cos(np.radians(arc_len + start_angle))
                endY = yc + (width/2)*np.sin(np.radians(arc_len + start_angle))
            else:
                start_angle = 270
                endX = xc + (height/2)*np.cos(np.radians(start_angle))
                endY = yc + (width/2)*np.sin(np.radians(start_angle))

            orientation = start_angle + arc_len
            arc = Arc([xc, yc], width, height, angle=start_angle, theta2=arc_len, capstyle='round', linestyle='-', lw=2.5, color="darkgreen")
            arrow_head = RegularPolygon((endX, endY), 3, height * 0.35, np.radians(orientation), color="darkgreen")
            ax.add_patch(arc)
            ax.add_patch(arrow_head)

        ax.axes.get_yaxis().set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        # ax.tick_params(left="off")

    def _update_loads(self):
        x0 = self._x0

        self._distributed_forces_x = [self._create_distributed_force(f) for f in self._distributed_loads_x()]
        self._distributed_forces_y = [self._create_distributed_force(f) for f in self._distributed_loads_y()]

        f_ax, f_ay, f_by = self.get_reaction_forces()
        pinned_support_load_x = PointLoadH(f_ax, self._pinned_support)
        pinned_support_load_y = PointLoadV(f_ay, self._pinned_support)
        rolling_support_load = PointLoadV(f_by, self._rolling_support)

        self._normal_forces = [-1*integrate(load, (x, x0, x)) for load in self._distributed_forces_x]
        self._normal_forces.extend(-1*self._effort_from_pointload(f) for f in self._point_loads_x())
        self._normal_forces.append(-1*self._effort_from_pointload(pinned_support_load_x))

        self._shear_forces = [integrate(load, (x, x0, x)) for load in self._distributed_forces_y]
        self._shear_forces.extend(self._effort_from_pointload(f) for f in self._point_loads_y())
        self._shear_forces.append(self._effort_from_pointload(pinned_support_load_y))
        self._shear_forces.append(self._effort_from_pointload(rolling_support_load))

        self._bending_moments = [integrate(load, (x, x0, x)) for load in self._shear_forces]
        self._bending_moments.extend(self._effort_from_pointload(f) for f in self._point_torques())

    def _create_distributed_force(self, load: DistributedLoadH or DistributedLoadV, shift: bool=True):
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
        expr, interval = load
        x0, x1 = interval
        expr = sympify(expr)
        if shift:
            expr.subs(x, x - x0)
        return Piecewise((0, x < x0), (0, x > x1), (expr, True))

    def _effort_from_pointload(self, load: PointLoadH or PointLoadV):
        """
        Create a sympy.Piecewise object representing the shear force caused by a
        point load.

        :param value: float or string with the numerical value of the point load.
        :param coord: x-coordinate on which the point load is applied.
        :return: sympy.Piecewise object with the value of the shear force produced
        by the provided point load.
        """
        value, coord = load
        return Piecewise((0, x < coord), (value, True))

    def _point_loads_x(self):
        for f in self._loads:
            if isinstance(f, PointLoadH):
                yield f

    def _point_loads_y(self):
        for f in self._loads:
            if isinstance(f, PointLoadV):
                yield f

    def _distributed_loads_x(self):
        for f in self._loads:
            if isinstance(f, DistributedLoadH):
                yield f

    def _distributed_loads_y(self):
        for f in self._loads:
            if isinstance(f, DistributedLoadV):
                yield f

    def _point_torques(self):
        for f in self._loads:
            if isinstance(f, PointTorque):
                yield f
