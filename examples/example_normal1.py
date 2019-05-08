# -*- coding: utf-8 -*-
"""Example 1: Shear force and bending moment diagrams for a beam subjected to
both point loads and distributed loads.
"""
import os
from beambending.beam import Beam, PointLoadH

def example_normal1():
    """Generate normal force introductory problem schematic"""
    beam = Beam(6)
    beam.rolling_support = 0  # x-coordinate of the rolling support
    beam.fixed_support = 3    # x-coordinate of the fixed support
    beam.add_loads([PointLoadH(5, 6)])  # 5kN pointing right, at x=6m
    fig = beam.plot_normal_force()
    
    # save the png and add it to the documentation
    mod_path = os.path.dirname(os.path.abspath(__file__))  # current module
    save_name = os.path.basename(__file__).replace('.py', '.png')  # file name
    save_path = os.path.join(mod_path, save_name)
    fig.savefig(save_path, transparent=True)


if __name__ == '__main__':  # call function when run as script
    example_normal1()
