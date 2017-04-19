import unittest
from numpy.testing import assert_array_almost_equal

from bending import Beam
from bending import DistributedLoad
from bending import PointLoad
from bending import PointTorque


class TestBeam(unittest.TestCase):
    def setUp(self):
        self.my_beam = Beam(10)
        self.assertEqual([], self.my_beam.load_inventory)
        self.my_beam.add_load(DistributedLoad([7, 0], 2, 6))
        self.my_beam.add_load(PointLoad([1, -45], 1))
        self.my_beam.add_load(PointTorque(80, 8))

    def test_beam_length_is_correctly_defined(self):
        self.my_beam.length = 10

    def test_loads_are_correctly_added_to_beam_inventory(self):
        self.assertAlmostEqual(56, self.my_beam.load_inventory[0].resultant.norm)
        self.assertAlmostEqual(2026**(1/2), self.my_beam.load_inventory[1].resultant.norm)
        self.assertAlmostEqual(8, self.my_beam.load_inventory[2].x_coord)

        # TODO: Add Beam supports (coords, and then calculate reaction forces)
        # TODO: Add functions for plotting M, V and N diagrams
        # TODO: Integrate in order to calculate beam inclination and deflection


class TestEvenlyDistributedLoad(unittest.TestCase):
    def setUp(self):
        coeffs = [3]
        a, b = 2, 6
        self.my_distributed_load = DistributedLoad(coeffs, a, b)

    def test_constant_distributed_load_is_correctly_defined(self):
        self.assertEqual([3], self.my_distributed_load.y_load.coeffs)
        self.assertEqual(2, self.my_distributed_load.x_left)
        self.assertEqual(6, self.my_distributed_load.x_right)

    def test_constant_distributed_load_is_correctly_evaluated(self):
        values, coords = [0, 3, 3, 3, 0], [0, 2, 4, 6, 8]
        for val, coord in zip(values, coords):
            self.assertEqual(val, self.my_distributed_load.value_at(coord))

    def test_resultant_norm_of_constant_distributed_load_is_correct(self):
        expected = PointLoad([0, 12], 4)
        assert_array_almost_equal(expected.vector2d, self.my_distributed_load.resultant.vector2d)
        self.assertAlmostEqual(expected.x_coord, self.my_distributed_load.resultant.x_coord)

    def test_moment_produced_by_constant_distributed_load_is_correct(self):
        self.assertEqual(48, self.my_distributed_load.moment)


class TestVariableDistributedLoad(unittest.TestCase):
    def setUp(self):
        coeffs = [5, -2, -1]
        left, right = 1, 5
        self.my_distributed_load = DistributedLoad(coeffs, left, right)

    def test_variable_distributed_load_is_correctly_evaluated(self):
        values, coords = [0, 2, 38, 0], [0, 2, 4, 6]
        for val, coord in zip(values, coords):
            self.assertEqual(val, self.my_distributed_load.value_at(coord))

    def test_resultant_norm_of_variable_distributed_load_is_correct(self):
        expected = PointLoad([0, 260/3], 267/65)
        assert_array_almost_equal(expected.vector2d, self.my_distributed_load.resultant.vector2d)
        self.assertAlmostEqual(expected.x_coord, self.my_distributed_load.resultant.x_coord)


class TestPointLoad(unittest.TestCase):
    def setUp(self):
        x_load, y_load = 15, 128
        x_coord = 7
        self.my_point_load = PointLoad([x_load, y_load], x_coord)

    def test_point_load_is_correctly_defined(self):
        self.assertEqual(7, self.my_point_load.x_coord)
        self.assertEqual(15, self.my_point_load.x)
        self.assertEqual(128, self.my_point_load.y)

    def test_norm_is_correctly_calculated(self):
        self.assertAlmostEqual(16609**(1/2), self.my_point_load.norm)

    def test_point_load_moment_is_correctly_calculated(self):
        self.assertEqual(896, self.my_point_load.moment)


class TestPointTorque(unittest.TestCase):
    """
    Torque applied at a point (counterclockwise positive). Consists of a 
    scalar magnitude and an application point 'x_coord'.
    """
    def setUp(self):
        magnitude = 231
        x_coord = 3
        self.my_point_torque = PointTorque(magnitude, x_coord)

    def test_point_torque_is_correctly_defined(self):
        self.assertEqual(231, self.my_point_torque.moment)
        self.assertEqual(3, self.my_point_torque.x_coord)

    def test_point_torque_moment_is_correct(self):
        self.assertEqual(231, self.my_point_torque.moment)

    def test_resultant_of_point_moment_is_zero(self):
        self.assertEqual(0, self.my_point_torque.resultant)