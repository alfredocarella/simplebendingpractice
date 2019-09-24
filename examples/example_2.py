# -*- coding: utf-8 -*-
"""Example 2: Shear force and bending moment diagrams for a beam subjected to
fancy polynomial distributed loads.
"""
import os
import matplotlib.pyplot as plt
from beambending import Beam, DistributedLoadV, PointLoadH, PointLoadV, x

def example_2():
    """Run example 2"""
    beam = Beam(9)
    beam.pinned_support = 2    # x-coordinate of the pinned support
    beam.rolling_support = 7  # x-coordinate of the rolling support
    eps = 1e-5
    beam.add_loads((
                    DistributedLoadV(-5+x - (x-2)**2 + (x-4)**3, (2+eps, 6.5)),
                    DistributedLoadV(-x**2*11/4, (0.0, 2)),
                    DistributedLoadV(-3+(x-6.5)**2*3/(2.5**2), (6.5+eps, 9)),
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
    example_2()
