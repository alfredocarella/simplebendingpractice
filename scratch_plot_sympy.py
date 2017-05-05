import matplotlib.pyplot as plt
import sympy
from sympy import integrate
from sympy import symbols
from sympy import lambdify
from sympy.functions.special.delta_functions import DiracDelta, Heaviside
import numpy as np


def my_heaviside(x_values):
    return (x_values >= 0) * 1.0


def my_diracdelta(x_values, *args):
    return x_values * 0


x = symbols('x')
f1 = x*x
f2 = integrate(f1)
f3 = integrate(DiracDelta(x-0.5))
f4 = DiracDelta(x-0.5)
f5 = sympy.diff(DiracDelta(x-0.5))

lam_f1 = lambdify(x, f1, modules=['numpy'])
lam_f2 = lambdify(x, f2, modules=['numpy'])
lam_f3 = lambdify(x, f3, modules=['numpy', {'Heaviside': my_heaviside, 'DiracDelta': my_diracdelta}])
lam_f4 = lambdify(x, f4, modules=['numpy', {'Heaviside': my_heaviside, 'DiracDelta': my_diracdelta}])
lam_f5 = lambdify(x, f5, modules=['numpy', {'Heaviside': my_heaviside, 'DiracDelta': my_diracdelta}])

x_vals = np.linspace(-5, 5, 1111)
y_vals = lam_f1(x_vals) + 3 * lam_f3(x_vals)
plt.plot(x_vals, y_vals)
plt.show()

# print(diff(diff(DiracDelta(x-0))))
# print(diff(DiracDelta(x-0)))
# print(DiracDelta(x-0))
# print(integrate(DiracDelta(x-0)))
print(integrate(DiracDelta(x-0) + x*x, (x, -1, 1)))