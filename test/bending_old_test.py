import unittest

from bending_old import Beam
from bending_old import DistributedLoad
from bending_old import PointLoad
from bending_old import PointTorque


class TestBeam(unittest.TestCase):
    def setUp(self):
        self.my_beam = Beam(10, (0, 9))

    def test_beam_is_correctly_created(self):
        self.assertEqual([], self.my_beam.load_inventory)
        self.assertEqual(10, self.my_beam.length)
        self.assertEqual(0, self.my_beam.fixed_coord)
        self.assertEqual(9, self.my_beam.rolling_coord)
        self.assertEqual([], self.my_beam.load_inventory)
        self.assertEqual((0, 0), self.my_beam.fixed_support)
        self.assertEqual(0, self.my_beam.rolling_support)

        self.assertEqual([0, 0], self.my_beam.distributed_loads)
        self.assertEqual([0, 0], self.my_beam.normal_and_shear_force)
        self.assertEqual(0, self.my_beam.bending_moment)

    def test_loads_correctly_added_to_inventory(self):
        self.my_beam.add_load(PointLoad((1, -45), 1))
        resultant = self.my_beam.load_inventory[0].resultant
        self.assertEqual((1, -45), (resultant.fx, resultant.fy))

        self.my_beam.add_load(DistributedLoad("0", "7*x", (2, 6)))
        resultant = self.my_beam.load_inventory[1].resultant
        self.assertEqual(56, resultant.fy)
        self.assertTupleEqual((0, 14), self.my_beam.load_inventory[1].value_at(4))

        self.my_beam.add_load(PointTorque(-90, 8))
        self.assertEqual(8, self.my_beam.load_inventory[2].x_coord)

    def test_reaction_forces_are_correct(self):
        self.my_beam.add_load(PointLoad((1, -45), 1))
        self.assertTupleEqual((-1, 40), self.my_beam.fixed_support)
        self.assertEqual(5, self.my_beam.rolling_support)

        self.my_beam.add_load(PointTorque(-90, 8))
        self.assertTupleEqual((-1, 30), self.my_beam.fixed_support)
        self.assertEqual(15, self.my_beam.rolling_support)

        self.my_beam.add_load(DistributedLoad(1, "3*x", (0, 10)))
        self.assertEqual(-11, self.my_beam.fixed_support[0])
        self.assertAlmostEqual(-80/9, self.my_beam.fixed_support[1])
        self.assertAlmostEqual(-865/9, self.my_beam.rolling_support)

    def test_numerical_sum_of_distributed_loads_is_correct(self):
        self.my_beam.add_load(DistributedLoad(5, 2, (0, 6)))
        self.my_beam.add_load(DistributedLoad("-x", -1.2, (0, 10)))
        self.assertEqual(1, self.my_beam.distributed_loads[0].subs("x", 4))
        self.assertEqual(0.8, self.my_beam.distributed_loads[1].subs("x", 0))
        self.assertEqual(-1.2, self.my_beam.distributed_loads[1].subs("x", 10))

    def test_normal_and_shear_forces_are_correct(self):
        self.my_beam.add_load(DistributedLoad(1, 1, (0, 10)))
        self.assertEqual(-40 / 9, self.my_beam.normal_and_shear_force[1].subs("x", 0))
        self.assertAlmostEqual(5 / 9, self.my_beam.normal_and_shear_force[1].subs("x", 5))
        self.assertEqual(0, self.my_beam.normal_and_shear_force[1].subs("x", 10))

        self.assertEqual(-10, self.my_beam.normal_and_shear_force[0].subs("x", 0))
        self.assertEqual(-5, self.my_beam.normal_and_shear_force[0].subs("x", 5))
        self.assertEqual(0, self.my_beam.normal_and_shear_force[0].subs("x", 10))


class TestSimpleBendingProblem(unittest.TestCase):
    def test_point_load_case_solved_correctly(self):
        self.my_beam = Beam(9, (2, 7))
        self.my_beam.add_load(DistributedLoad(0.0, -20, (0, 2)))
        self.my_beam.add_load(DistributedLoad(0.0, -10, (3, 9)))
        self.my_beam.add_load(PointLoad((1.0, -20), 3))
        self.assertAlmostEqual(36, self.my_beam.normal_and_shear_force[1].subs("x", 2.0))
        # Source: "Mathalino" [This case fails consistently]
        # https://www.mathalino.com/reviewer/mechanics-and-strength-of-materials/solution-to-problem-448-relationship-between-load-shear
        print(self.my_beam.bending_moment.subs("x", 7.0))
        self.assertEqual(-20, self.my_beam.bending_moment.subs("x", 7.0))
        #
        # self.my_beam.plot()



