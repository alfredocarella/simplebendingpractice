# -*- coding: utf-8 -*-
"""Example 1: Shear force and bending moment diagrams for a beam subjected to
both point loads and distributed loads.
"""
import os
import sympy
from beambending.beam import Beam, DistributedLoadV, PointLoadH, PointLoadV

def example_1():
    """Run example 1"""
    # x = sympy.symbols("x")  # uncomment if you use variable distributed loads
    beam = Beam(9)
    beam.fixed_support = 2    # x-coordinate of the fixed support
    beam.rolling_support = 7  # x-coordinate of the rolling support
    beam.add_loads((
                    PointLoadH(10, 3),  # 10kN pointing right, at x=3m
                    PointLoadV(-20, 3),  # 20kN downwards, at x=3m
                    DistributedLoadV(-10, (3, 9)),  # 10 kN/m, downward, for 3m <= x <= 9m
                    DistributedLoadV(-20, (0, 2)),  # 20 kN/m downwards, for 0m <= x <= 2m
                ))
    fig = beam.plot()

    # save the png and add it to the documentation
    mod_path = os.path.dirname(os.path.abspath(__file__))  # current module
    save_name = os.path.basename(__file__).replace('.py', '.png')  # file name
    save_path = os.path.join(mod_path, save_name)
    fig.savefig(save_path)


if __name__ == '__main__':  # call function when run as script
    example_1()
