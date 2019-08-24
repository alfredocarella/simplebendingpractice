# -*- coding: utf-8 -*-
"""Example 1: Shear force and bending moment diagrams for a beam subjected to
both point loads and distributed loads.
"""
import os
from beambending import Beam, DistributedLoadV, PointLoadH, PointLoadV, x

def example_1():
    """Run example 1"""
    beam = Beam(9)  # Initialize a Beam object of length 9 m
    beam.pinned_support = 2    # x-coordinate of the pinned support
    beam.rolling_support = 7  # x-coordinate of the rolling support
    beam.add_loads((
                    PointLoadH(10, 3),  # 10 kN pointing right, at x=3 m
                    PointLoadV(-20, 3),  # 20 kN downwards, at x=3 m
                    DistributedLoadV(-10, (3, 9)),  # 10 kN/m, downwards, for 3 m <= x <= 9 m
                    DistributedLoadV(-20 + x**2, (0, 2)),  # variable load, for 0 <= x <= 2 m
                ))
    fig = beam.plot()

    # save the png and add it to the documentation
    mod_path = os.path.dirname(os.path.abspath(__file__))  # current module
    save_name = os.path.basename(__file__).replace('.py', '.svg')  # file name
    save_path = os.path.join(mod_path, save_name)
    fig.savefig(save_path, transparent=True)


if __name__ == '__main__':  # call function when run as script
    example_1()
