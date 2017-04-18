import unittest
from bending import DistributedLoad
from bending import Beam


class TestDistributedLoad(unittest.TestCase):
    def setUp(self):
        coeffs = [3]
        a, b = 2, 6
        self.my_distributed_load = DistributedLoad(coeffs, a, b)

    def test_constant_distributed_load_is_correctly_defined(self):
        self.assertEqual([3], self.my_distributed_load.poly.coeffs)
        self.assertEqual(2, self.my_distributed_load.left)
        self.assertEqual(6, self.my_distributed_load.right)

    def test_constant_distributed_load_is_correctly_evaluated(self):
        values, coords = [0, 3, 3, 3, 0], [0, 2, 4, 6, 8]
        for val, coord in zip(values, coords):
            self.assertEqual(val, self.my_distributed_load.value_at(coord))

    def test_resultant_of_constant_distributed_load_is_correct(self):
        self.assertEqual(PointLoad([0, 12], 4), self.my_distributed_load.resultant)


class TestBeam(unittest.TestCase):
    def setUp(self):
        self.my_beam = Beam(10)

    def test_beam_length_is_correctly_defined(self):
        self.my_beam.length = 10
