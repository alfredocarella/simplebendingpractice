from contextlib import contextmanager
import numpy as np
from numpy.testing import assert_allclose
import pytest
from sympy import lambdify

from beambending import Beam, DistributedLoadH, DistributedLoadV, PointLoadH, PointLoadV, PointTorque, x


def test_beam_is_correctly_created():
    span = 9
    my_beam = Beam(span)
    assert my_beam._x0 == 0
    assert my_beam._x1 == 9


def test_beam_supports_are_correctly_added():
    span = 9
    my_beam = Beam(span)
    my_beam.rolling_support = 7

    assert my_beam._pinned_support == 2
    assert my_beam._rolling_support == 7


def test_beam_supports_must_be_within_span():
    span = 9
    my_beam = Beam(span)

    with pytest.raises(ValueError):
        my_beam.pinned_support = -3

    with pytest.raises(ValueError):
        my_beam.rolling_support = 10


def test_beam_loads_are_correctly_added():
    span = 9
    my_beam = Beam(span)

    loads = [DistributedLoadV(-20, (0, 2)),
             PointLoadV(-20, 3),
             DistributedLoadV("-10", (3, 9)),
             PointLoadH(15, 5),
             DistributedLoadV("-2*x", (1, 3))
            ]
    my_beam.add_loads(loads)

    assert my_beam._loads[0] == DistributedLoadV(-20, (0, 2))
    assert my_beam._loads[1] == PointLoadV(-20, 3)
    assert my_beam._loads[2] == DistributedLoadV("-10", (3, 9))
    assert my_beam._loads[3] == PointLoadH(15, 5)
    assert my_beam._loads[4] == DistributedLoadH("-2*x", (1, 3))

    with pytest.raises(TypeError):
        my_beam.add_loads((10, (3, 9)))


@contextmanager
def defined_canonical_beam(span=9, pinned=2, rolling=7):
    my_beam = Beam(span)
    my_beam.pinned_support = pinned
    my_beam.rolling_support = rolling
    my_beam.add_loads([DistributedLoadV("-10", (3, 9)),
                       PointLoadV(-20, 3),
                       DistributedLoadV(-20, (0, 2)),
                       PointLoadH(15, 5),
                       DistributedLoadH("-2", (7, 9))])
    x_vec = np.linspace(0, 9, 19)

    try:
        yield my_beam, x, x_vec
    finally:
        pass


def test_beam_distributed_loads_are_correct():
    with defined_canonical_beam() as (the_beam, x, x_vec):
        distributed_load_sample = lambdify(x, sum(the_beam._distributed_forces_y), "numpy")(x_vec)
        expected = [-20] * 5 + [0] + [-10] * 13
        np.testing.assert_allclose(distributed_load_sample, expected)


def test_beam_normal_forces_are_correct():
    with defined_canonical_beam() as (the_beam, x, x_vec):
        normal_force_lambda = lambdify(x, sum(the_beam._normal_forces), "numpy")
        normal_force_sample = [normal_force_lambda(t) for t in x_vec]
        expected = [0, 0, 0, 0, 11, 11, 11, 11, 11, 11, -4, -4, -4, -4, -4, -3, -2, -1, 0]
        np.testing.assert_allclose(normal_force_sample, expected)


def test_beam_shear_forces_are_correct():
    with defined_canonical_beam() as (the_beam, x, x_vec):
        shear_force_lambda = lambdify(x, sum(the_beam._shear_forces), "numpy")
        shear_force_sample = [shear_force_lambda(t) for t in x_vec]
        expected = [0, -10, -20, -30, 36, 36, 16, 11, 6, 1, -4, -9, -14, -19, 20, 15, 10, 5, 0]
        np.testing.assert_allclose(shear_force_sample, expected)


def test_beam_bending_moments_are_correct():
    with defined_canonical_beam() as (the_beam, x, x_vec):
        bending_moment_lambda = lambdify(x, sum(the_beam._bending_moments), "numpy")
        bending_moment_sample = [bending_moment_lambda(t) for t in x_vec]
        expected = [0, -2.5, -10, -22.5, -40, -22, -4, 2.75, 7, 8.75, 8, 4.75, -1, -9.25, -20, -11.25, -5, -1.25, 0]
        np.testing.assert_allclose(bending_moment_sample, expected)


def test_beam_point_moments_work_correctly():
    with defined_canonical_beam() as (the_beam, x, x_vec):
        the_beam._loads = []
        the_beam.add_loads([PointTorque(30, 4)])
        bending_moment_lambda = lambdify(x, sum(the_beam._bending_moments), "numpy")
        bending_moment_sample = [bending_moment_lambda(t) for t in x_vec]
        expected = [0, 0, 0, 0, 0, -3, -6, -9, 18, 15, 12, 9, 6, 3, 0, 0, 0, 0, 0]
        assert_allclose(bending_moment_sample, expected)

