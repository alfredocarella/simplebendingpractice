import matplotlib.pyplot as plt
import numpy as np
from sympy import integrate, Piecewise, symbols, lambdify

from crunching import get_reaction_forces, plot_analytical, create_distributed_load, create_point_load

plt.rc('text', usetex=True)

x0, x1 = 0, 9
x = symbols("x")
x_axis = np.linspace(x0, x1, (x1-x0)*1000+1)

# dist_load = 0
# dist_load += create_distributed_load(-20, (0, 2))
# print(integrate(dist_load, (x, x0, x1)))
# dist_load += create_distributed_load(-10, (3, 9), shift=True)
# print(integrate(dist_load, (x, x0, x1)))

dist_loads = []
dist_loads.append(create_distributed_load(-20, (0, 2)))
dist_loads.append(create_distributed_load(-10, (3, 9), shift=True))

point_load_x = 3
point_load_kN = -20




# -------- Calculate reaction forces at supports -------- #
F_Rx = 0
F_Ry = sum(integrate(load, (x, x0, x1)) for load in dist_loads) + point_load_kN
M_R = sum(integrate(load * x, (x, x0, x1)) for load in dist_loads) + point_load_kN * point_load_x
print("F_Ry:\t{0}\nM_R:\t{1}".format(F_Ry, M_R))
xA, xB = 2, 7

support_coords = xA, xB
resultant_force = F_Rx, F_Ry
F_Ax, F_Ay, F_By = get_reaction_forces(support_coords, resultant_force, M_R)
print("F_Ax:\t{0}\nF_Ay:\t{1}\nF_By:\t{2}".format(F_Ax, F_Ay, F_By))
# -------- Calculate reaction forces at supports -------- #

shear_forces = [integrate(load, (x, x0, x)) for load in dist_loads]
shear_forces.append(create_point_load(point_load_kN, point_load_x))
shear_forces.append(create_point_load(F_Ay, xA))
shear_forces.append(create_point_load(F_By, xB))


# bending_moment = integrate(sum(shear_forces))
bending_moments = [integrate(load, (x, x0, x)) for load in shear_forces]


fig = plt.figure(figsize=(6, 10))
fig.subplots_adjust(hspace=0.4)

ax1 = fig.add_subplot(3, 1, 1)
plot01_params = {'filename':"foo01",
               'maxmin_hline':True,
               'x_units':"m",
               'y_units':'kN / m',
               'ylabel':"Distributed loads",
               'facecolor':"b",
               'title':"LATEX TEST $- \\frac{2 \\sqrt{11}}{5} + \\frac{23}{5}$"}
plot_analytical(ax1, x_axis, sum(dist_loads), **plot01_params)

ax2 = fig.add_subplot(3, 1, 2)
plot02_params = {'filename':"foo02",
                 'maxmin_hline':True,
                 'x_units':"m",
                 'y_units':'kN',
                 'ylabel':"Shear force",
                 'facecolor':"r"}
plot_analytical(ax2, x_axis, sum(shear_forces), **plot02_params)

ax3 = fig.add_subplot(3, 1, 3)
plot03_params = {'filename':"foo03",
                 'maxmin_hline':True,
                 'x_units':"m",
                 'y_units':'kN \cdot m',
                 'ylabel':"Bending moment",
                 'facecolor':"y"}
plot_analytical(ax3, x_axis, sum(bending_moments), **plot03_params)

plt.savefig(fname="output/test01.pdf")
# exit()
