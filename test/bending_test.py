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
        self.assertEqual(0, self.my_distributed_load.value_at(0))
        self.assertEqual(3, self.my_distributed_load.value_at(2))
        self.assertEqual(3, self.my_distributed_load.value_at(4))
        self.assertEqual(3, self.my_distributed_load.value_at(6))
        self.assertEqual(0, self.my_distributed_load.value_at(8))


class TestBeam(unittest.TestCase):
    def setUp(self):
        self.my_beam = Beam(10)

    def test_beam_length_is_correctly_defined(self):
        self.my_beam.length = 10
