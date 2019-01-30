import numpy as np
from numpy.testing import assert_allclose
import pytest
import sympy

from beambending import beam
from contextlib import contextmanager


def test_beam_is_correctly_created():
    span = (0, 9)
    my_beam = beam.Beam(span)
    assert my_beam._x0 == 0
    assert my_beam._x1 == 9


def test_beam_supports_are_correctly_added():
    span = (0, 9)
    my_beam = beam.Beam(span)
    my_beam.rolling_support(7)

    assert my_beam._fixed_support == 2
    assert my_beam._rolling_support == 7


def test_beam_supports_must_be_within_span():
    span = (0, 9)
    my_beam = beam.Beam(span)

    with pytest.raises(ValueError):
        my_beam.fixed_support(-3)

    with pytest.raises(ValueError):
        my_beam.rolling_support(10)


def test_beam_loads_are_correctly_added():
    span = (0, 9)
    my_beam = beam.Beam(span)

    my_beam.distributed_load(-20, (0, 2))
    my_beam.point_load(-20, 3)
    my_beam.distributed_load("-10", (3, 9))
    assert my_beam._loads[0] == beam.DistributedLoad(-20, (0, 2))
    assert my_beam._loads[1] == beam.PointLoad(-20, 3)
    assert my_beam._loads[2] == beam.DistributedLoad("-10", (3, 9))


def test_beam_loads_are_added_from_list():
    span = (0, 9)
    my_beam = beam.Beam(span)

    loads = (beam.DistributedLoad("-10", (3, 9)),
             beam.PointLoad(-20, 3),
             beam.DistributedLoad(-20, (0, 2)))

    my_beam.add_loads(loads)
    assert my_beam._loads[0] == beam.DistributedLoad("-10", (3, 9))
    assert my_beam._loads[1] == beam.PointLoad(-20, 3)
    assert my_beam._loads[2] == beam.DistributedLoad(-20, (0, 2))

    with pytest.raises(TypeError):
        my_beam.add_loads((10, (3, 9)))


@contextmanager
def defined_canonical_beam(span=(0, 9), fixed=2, rolling=7):
    my_beam = beam.Beam(span)
    my_beam.fixed_support(fixed)
    my_beam.rolling_support(rolling)
    my_beam.add_loads([beam.DistributedLoad("-10", (3, 9)),
                       beam.PointLoad(-20, 3),
                       beam.DistributedLoad(-20, (0, 2))])
    x = sympy.symbols("x")
    x_vec = np.linspace(0, 9, 19)

    try:
        yield my_beam, x, x_vec
    finally:
        pass


def test_beam_distributed_loads_are_correct():
    with defined_canonical_beam() as (the_beam, x, x_vec):
        distributed_load_sample = sympy.lambdify(x, the_beam.get_distributed_force(), "numpy")(x_vec)
        expected = [-20] * 5 + [0] + [-10] * 13
        np.testing.assert_allclose(distributed_load_sample, expected)


def test_beam_shear_forces_are_correct():
    with defined_canonical_beam() as (the_beam, x, x_vec):
        shear_force_sample = sympy.lambdify(x, the_beam.get_shear_force(), "numpy")(x_vec)
        expected = [0, -10, -20, -30, 36, 36, 16, 11, 6, 1, -4, -9, -14, -19, 20, 15, 10, 5, 0]
        np.testing.assert_allclose(shear_force_sample, expected)


def test_beam_bending_moments_are_correct():
    with defined_canonical_beam() as (the_beam, x, x_vec):
        bending_moment_sample = sympy.lambdify(x, the_beam.get_bending_moment(), "numpy")(x_vec)
        expected = [0, -2.5, -10, -22.5, -40, -22, -4, 2.75, 7, 8.75, 8, 4.75, -1, -9.25, -20, -11.25, -5, -1.25, 0]
        np.testing.assert_allclose(bending_moment_sample, expected)


