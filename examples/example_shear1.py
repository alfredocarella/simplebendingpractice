# -*- coding: utf-8 -*-
"""Example 1: Shear force and bending moment diagrams for a beam subjected to
both point loads and distributed loads.
"""
import os
import matplotlib.pyplot as plt
from beambending import Beam, PointLoadV

def example_shear1():
    """Generate shear force introductory problem schematic"""
    my_beam = Beam(6)
    my_beam.rolling_support = 0  # x-coordinate of the rolling support
    my_beam.pinned_support = 3    # x-coordinate of the pinned support
    my_beam.add_loads([PointLoadV(10, 6)])  # 10kN pointing upwards, at x=6m
    fig = plt.figure()
    my_beam.plot_shear_force(fig.add_subplot(2, 1, 1))
    my_beam.plot_bending_moment(fig.add_subplot(2, 1, 2))

    
    # save the png and add it to the documentation
    mod_path = os.path.dirname(os.path.abspath(__file__))  # current module
    save_name = os.path.basename(__file__).replace('.py', '.png')  # file name
    save_path = os.path.join(mod_path, save_name)
    fig.savefig(save_path, transparent=True)


if __name__ == '__main__':  # call function when run as script
    example_shear1()
