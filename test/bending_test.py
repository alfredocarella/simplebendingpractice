import unittest
from numpy.testing import assert_array_almost_equal

from bending import Beam
from bending import DistributedLoad
from bending import PointLoad


class TestBeam(unittest.TestCase):
    def setUp(self):
        self.my_beam = Beam(10)

    def test_beam_length_is_correctly_defined(self):
        self.my_beam.length = 10


class TestDistributedLoad(unittest.TestCase):
    def setUp(self):
        coeffs = [3]
        a, b = 2, 6
        self.my_distributed_load = DistributedLoad(coeffs, a, b)

    def test_constant_distributed_load_is_correctly_defined(self):
        self.assertEqual([3], self.my_distributed_load.y_load.coeffs)
        self.assertEqual(2, self.my_distributed_load.left)
        self.assertEqual(6, self.my_distributed_load.right)

    def test_constant_distributed_load_is_correctly_evaluated(self):
        values, coords = [0, 3, 3, 3, 0], [0, 2, 4, 6, 8]
        for val, coord in zip(values, coords):
            self.assertEqual(val, self.my_distributed_load.value_at(coord))

    def test_resultant_norm_of_constant_distributed_load_is_correct(self):
        expected = PointLoad([0, 12], 4)
        assert_array_almost_equal(expected.vector2d, self.my_distributed_load.resultant.vector2d)
        self.assertAlmostEqual(expected.x_coord, self.my_distributed_load.resultant.x_coord)


class TestPointLoad(unittest.TestCase):
    def test_point_load_is_correctly_defined(self):
        x_load, y_load = 15, 128
        x_coord = 7
        self.my_point_load = PointLoad([x_load, y_load], x_coord)
        self.assertEqual(7, self.my_point_load.x_coord)
        self.assertEqual(15, self.my_point_load.x)
        self.assertEqual(128, self.my_point_load.y)
        self.assertAlmostEqual(16609**(1/2), self.my_point_load.norm)

