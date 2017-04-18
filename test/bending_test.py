import unittest
from bending import Distload
from bending import Beam


class TestDistload(unittest.TestCase):
    def setUp(self):
        ppar = [5, 4, 3, -10]
        self.q = Distload(ppar)

    def test_distload_polynomial_evaluates_to_right_value(self):
        self.assertEqual(52, self.q(2))


class TestBeam(unittest.TestCase):
    def setUp(self):
        self.my_beam = Beam(10)

    def test_beam_length_is_correctly_defined(self):
        self.my_beam.length = 10
