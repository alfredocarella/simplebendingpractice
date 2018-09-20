import matplotlib.pyplot as plt
import numpy as np
from sympy import integrate, symbols

from crunching import get_reaction_forces, plot_analytical, create_distributed_load, shear_from_pointload, DistributedLoad, PointLoad, distributed, point

# User input
beam_span = (0, 9)
fixed_support = 2
rolling_support = 7

loads = [PointLoad(-20, 3),
         DistributedLoad(-20, (0, 2)),
         DistributedLoad("-10", (3, 9))]


# Calculate reaction forces at supports
x = symbols("x")
x0, x1 = beam_span
xA, xB = fixed_support, rolling_support

F_Rx = 0
dist_forces = [create_distributed_load(*f) for f in distributed(loads)]
F_Ry = sum(integrate(load, (x, x0, x1)) for load in dist_forces) + \
       sum(f.force for f in point(loads))
M_R = sum(integrate(load * x, (x, x0, x1)) for load in dist_forces) + \
      sum(f.force * f.coord for f in point(loads))
support_coords = xA, xB
resultant_force = F_Rx, F_Ry
F_Ax, F_Ay, F_By = get_reaction_forces(support_coords, resultant_force, M_R)

shear_forces = [integrate(load, (x, x0, x)) for load in dist_forces]
shear_forces.extend(shear_from_pointload(*f) for f in point(loads))
shear_forces.append(shear_from_pointload(F_Ay, xA))
shear_forces.append(shear_from_pointload(F_By, xB))

bending_moments = [integrate(load, (x, x0, x)) for load in shear_forces]


# Plotting
fig = plt.figure(figsize=(6, 10))
fig.subplots_adjust(hspace=0.4)
x_axis = np.linspace(x0, x1, (x1-x0)*1000+1)

ax1 = fig.add_subplot(4, 1, 2)
plot01_params = {'ylabel':"Distributed loads", 'yunits':'kN / m',
                 # 'xlabel':"Beam axis", 'xunits':"m",
                 'color':"b",
                 'title': r"LATEX TEST $- \frac{2 \sqrt{11}}{5} + \frac{23}{5}$"}
plot_analytical(ax1, x_axis, sum(dist_forces), **plot01_params)

ax2 = fig.add_subplot(4, 1, 3)
plot02_params = {'ylabel':"Shear force", 'yunits':'kN',
                 # 'xlabel':"Beam axis", 'xunits':"m",
                 'color':"r"}
plot_analytical(ax2, x_axis, sum(shear_forces), **plot02_params)

ax3 = fig.add_subplot(4, 1, 4)
plot03_params = {'ylabel':"Bending moment", 'yunits':'kN \cdot m',
                 'xlabel':"Beam axis", 'xunits':"m",
                 'color':"y"}
plot_analytical(ax3, x_axis, sum(bending_moments), **plot03_params)

plt.savefig(fname="output/test01.pdf")

