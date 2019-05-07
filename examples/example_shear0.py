# -*- coding: utf-8 -*-
"""Example 1: Shear force and bending moment diagrams for a beam subjected to
both point loads and distributed loads.
"""
import os
from beambending.beam import Beam, PointLoadV

def example_shear0():
    """Generate shear force introductory problem schematic"""
    my_beam = Beam(6)
    my_beam.rolling_support = 0  # x-coordinate of the rolling support
    my_beam.fixed_support = 3    # x-coordinate of the fixed support
    my_beam.add_loads([PointLoadV(10, 6)])  # 10kN pointing upwards, at x=6m
    fig = my_beam.plot_beam_diagram()
    ax = fig.gca()
    ax.text(0, -1.35, r'A', ha='center', va='top')
    ax.text(3, -1.35, r'B', ha='center', va='top')
    ax.text(5.9, -1.2, r'$P_1=10kN$', ha='right', va='top', color='darkgreen')
    ax.axvline(x=2, linestyle='--', color="k", alpha=0.5)
    ax.text(2, 0.5, r'Section 1-1', rotation=90, ha='right', va='bottom')
    ax.axvline(x=4, linestyle='--', color="k", alpha=0.5)
    ax.text(4, 0.5, r'Section 2-2', rotation=90, ha='right', va='bottom')
    ax.axvline(x=6, linestyle='--', color="k", alpha=0.5)
    ax.text(6, 0.5, r'Section 3-3', rotation=90, ha='right', va='bottom')
    
    # save the png and add it to the documentation
    mod_path = os.path.dirname(os.path.abspath(__file__))  # current module
    save_name = os.path.basename(__file__).replace('.py', '.png')  # file name
    save_path = os.path.join(mod_path, save_name)
    fig.savefig(save_path)


if __name__ == '__main__':  # call function when run as script
    example_shear0()
