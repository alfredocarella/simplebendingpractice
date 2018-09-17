from numpy.testing import assert_allclose
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
