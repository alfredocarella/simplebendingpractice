import unittest
from numpy.testing import assert_array_almost_equal

from bending import Beam
from bending import DistributedLoad
from bending import PointLoad
from bending import PointTorque
from bending import plot_numerical


class TestBeam(unittest.TestCase):
    def setUp(self):
        self.my_beam = Beam(10, [0, 9], plot_resolution=1000)
        self.assertEqual([], self.my_beam.load_inventory)

    def test_beam_length_is_correctly_defined(self):
        self.my_beam.length = 10

    def test_fixed_and_rolling_support_coordinates_are_correctly_defined(self):
        self.assertEqual(0, self.my_beam.fixed_coord)
        self.assertEqual(9, self.my_beam.rolling_coord)

    def test_loads_are_correctly_added_to_load_inventory(self):
        self.my_beam.add_load(DistributedLoad(([0], [7, 0]), [2, 6]))
        self.my_beam.add_load(PointLoad([1, -45], 1))
        self.my_beam.add_load(PointTorque(80, 8))
        self.assertAlmostEqual(56, self.my_beam.load_inventory[0].resultant.norm)
        self.assertAlmostEqual(2026**(1/2), self.my_beam.load_inventory[1].resultant.norm)
        self.assertAlmostEqual(8, self.my_beam.load_inventory[2].x_coord)

    def test_reaction_forces_are_correct(self):
        self.my_beam.add_load(PointLoad([1, -45], 1))
        self.check_reaction_forces([[-1, 40.0], 5])
        self.my_beam.add_load(PointTorque(-90, 8))
        self.check_reaction_forces([[-1, 30.0], 15])
        self.my_beam.add_load(DistributedLoad(([1], [3, 0]), [0, 10]))
        self.check_reaction_forces([[-11, -80/9], -865/9])

    def test_numerical_sum_of_distributed_loads_is_correct(self):
        self.my_beam.add_load(DistributedLoad(([0], [2]), [0, 6]))
        self.my_beam.add_load(DistributedLoad(([0], [-1.2]), [0, 10]))
        self.assertEqual(0.8, self.my_beam.distributed_loads[2, 0])
        self.assertEqual(-1.2, self.my_beam.distributed_loads[2, -1])

    def test_shear_forces_are_correct(self):
        self.my_beam.add_load(DistributedLoad(([0], [1]), [0, 10]))
        self.assertEqual(-40/9, self.my_beam.shear_force[1, 0])
        self.assertEqual(0, self.my_beam.shear_force[1, -1])

    def test_normal_forces_are_correct(self):
        self.my_beam.add_load(DistributedLoad(([1], [1]), [0, 10]))
        self.assertEqual(-10, self.my_beam.normal_force[-1, 0])
        self.assertAlmostEqual(-5, self.my_beam.normal_force[1, 500], places=1)
        self.assertAlmostEqual(0, self.my_beam.normal_force[1, -1])

    def test_bending_moment_is_zero_at_the_ends(self):
        self.my_beam.add_load(DistributedLoad(([0], [1]), [0, 10]))
        self.my_beam.add_load(PointTorque(-8, 5))
        self.assertEqual(0, self.my_beam.bending_moment[1, 0])
        self.assertAlmostEqual(0, self.my_beam.bending_moment[1, -1], places=1)
        # TODO: Integrate in order to calculate beam inclination and deflection
        # TODO: Use gaussian quadrature or even better, analytical integration

    def check_reaction_forces(self, expected):
        fixed_load, rolling_load = expected
        print(self.my_beam.fixed_load)
        print(fixed_load)
        assert_array_almost_equal(fixed_load, self.my_beam.fixed_load)
        self.assertAlmostEqual(rolling_load, self.my_beam.rolling_load)


class TestEvenlyDistributedLoad(unittest.TestCase):
    def setUp(self):
        coeffs = ([0], [3])
        start_end = (2, 6)
        self.my_distributed_load = DistributedLoad(coeffs, start_end)

    def test_evenly_distributed_load_is_correctly_defined(self):
        self.assertEqual([3], self.my_distributed_load.y_load.coeffs)
        self.assertEqual(2, self.my_distributed_load.x_left)
        self.assertEqual(6, self.my_distributed_load.x_right)

    def test_evenly_distributed_load_is_correctly_evaluated(self):
        values, coords = ([0, 0, 0, 0, 0], [0, 3, 3, 3, 0]), [0, 2, 4, 6, 8]
        assert_array_almost_equal(values, self.my_distributed_load.value_at(coords))

    def test_resultant_norm_of_evenly_distributed_load_is_correct(self):
        expected = PointLoad([0, 12], 4)
        assert_array_almost_equal(expected.vector2d, self.my_distributed_load.resultant.vector2d)
        self.assertAlmostEqual(expected.x_coord, self.my_distributed_load.resultant.x_coord)

    def test_moment_produced_by_evenly_distributed_load_is_correct(self):
        self.assertEqual(48, self.my_distributed_load.moment)


class TestVariableDistributedLoad(unittest.TestCase):
    def setUp(self):
        coeffs = [[1], [5, -2, -1]]
        start_end = (1, 5)
        self.my_distributed_load = DistributedLoad(coeffs, start_end)

    def test_variable_distributed_load_is_correctly_evaluated(self):
        values, coords = [(0, 1, 1, 0), (0, 2, 38, 0)], [0, 2, 4, 6]
        assert_array_almost_equal(values, self.my_distributed_load.value_at(coords))

    def test_resultant_norm_of_variable_distributed_load_is_correct(self):
        expected = PointLoad([4, 260/3], 267/65)
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
        self.assertEqual(0, self.my_point_torque.resultant.norm)