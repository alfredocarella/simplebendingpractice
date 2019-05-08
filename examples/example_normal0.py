# -*- coding: utf-8 -*-
"""Example 1: Shear force and bending moment diagrams for a beam subjected to
both point loads and distributed loads.
"""
import os
from beambending.beam import Beam, PointLoadH

def example_normal0():
    """Generate normal force introductory problem schematic"""
    beam = Beam(6)
    beam.rolling_support = 0  # x-coordinate of the rolling support
    beam.fixed_support = 3    # x-coordinate of the fixed support
    beam.add_loads([PointLoadH(5, 6)])  # 5kN pointing right, at x=6m
    fig = beam.plot_beam_diagram()
    ax = fig.gca()
    ax.text(0, -1.35, r'A', ha='center', va='top')
    ax.text(3, -1.35, r'B', ha='center', va='top')
    ax.text(6, -0.5, r'$F_1=5kN$', ha='right', va='top', color='darkgreen')
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
    fig.savefig(save_path, transparent=True)


if __name__ == '__main__':  # call function when run as script
    example_normal0()
