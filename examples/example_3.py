# -*- coding: utf-8 -*-
"""Example 3: Shear force and bending moment diagrams for a beam subjected to
a point torque.
"""
import os
import matplotlib.pyplot as plt
from beambending import Beam, DistributedLoadV, PointLoadH, PointLoadV, PointTorque, x

def example_3():
    """Run example 3"""
    beam = Beam(9)
    beam.pinned_support = 2    # x-coordinate of the pinned support
    beam.rolling_support = 7  # x-coordinate of the rolling support
    beam.add_loads((
                    PointLoadV(3, 6),
                    PointTorque(30, 4),
                ))
    fig = plt.figure(figsize=(6, 7.5))
    fig.subplots_adjust(hspace=0.4)

    ax1 = fig.add_subplot(3, 1, 1)
    beam.plot_beam_diagram(ax1)

    ax2 = fig.add_subplot(3, 1, 2)
    beam.plot_shear_force(ax2)

    ax3 = fig.add_subplot(3, 1, 3)
    beam.plot_bending_moment(ax3)

    # save the png and add it to the documentation
    mod_path = os.path.dirname(os.path.abspath(__file__))  # current module
    save_name = os.path.basename(__file__).replace('.py', '.png')  # file name
    save_path = os.path.join(mod_path, save_name)
    fig.savefig(save_path, transparent=True)


if __name__ == '__main__':  # call function when run as script
    example_3()
