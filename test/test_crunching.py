import numpy as np
from numpy.testing import assert_allclose
import sympy

import crunching  # calculate_reaction_forces, plot_analytical


# import matplotlib.pyplot as plt
# from sympy import integrate, Piecewise, symbols, lambdify
# plt.rc('text', usetex=True)


def test_get_reaction_forces():
    x_coords = (2, 7)
    FRx, FRy, M_R = -20, -150, -505
    F_Ax, F_Ay, F_By = crunching.get_reaction_forces(x_coords, (FRx, FRy), M_R)
    expected = 20, 109, 41
    assert_allclose((F_Ax, F_Ay, F_By), expected, rtol=1e-5)


def test_calculate_diagrams():
    # User input
    beam_span = (0, 9)
    fixed_support = 2
    rolling_support = 7
    loads = [crunching.PointLoad(-20, 3),
             crunching.DistributedLoad(-20, (0, 2)),
             crunching.DistributedLoad("-10", (3, 9))]

    x0, x1, dist_forces, shear_forces, bending_moments = crunching.calculate_diagrams(beam_span, fixed_support, rolling_support, loads)
    x_vec = np.linspace(0, 9, 19)

    x = sympy.symbols('x')

    distributed_calc = sympy.lambdify(x, sum(dist_forces), "numpy")(x_vec)
    distributed_expected = [-20]*5 + [0] + [-10]*13
    np.testing.assert_allclose(distributed_calc, distributed_expected)

    shear_calc = sympy.lambdify(x, sum(shear_forces), "numpy")(x_vec)
    shear_expected = [0, -10, -20, -30, 36, 36, 16, 11, 6, 1, -4, -9, -14, -19, 20, 15, 10, 5, 0]
    np.testing.assert_allclose(shear_calc, shear_expected)

    bending_calc = sympy.lambdify(x, sum(bending_moments), "numpy")(x_vec)
    bending_expected = [0, -2.5, -10, -22.5, -40, -22, -4, 2.75, 7, 8.75, 8, 4.75, -1, -9.25, -20, -11.25, -5, -1.25, 0]
    np.testing.assert_allclose(bending_calc, bending_expected)


def test_beam_is_correctly_created():
    span = [0, 9]
    my_beam = crunching.Beam(span)
    assert my_beam._x0 == 0
    assert my_beam._x1 == 9


def test_beam_supports_are_correctly_added():
    span = (0, 9)
    my_beam = crunching.Beam(span)
    my_beam.rolling_support(7)

    assert my_beam._fixed_support == 2
    assert my_beam._rolling_support == 7


