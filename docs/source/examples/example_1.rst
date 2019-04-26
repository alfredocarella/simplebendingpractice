.. Example 1

Beam with one point load and two distributed loads
==================================================

This example demonstrates some functionality of the ´´beambending´´ package.

Specifications
--------------
A beam resting on two supports at x=2 and x=7, with the following applied loads:

* a downward force of 20kN at x=3;
* a force of 10kN pointing right, also at x=3;
* a downward distributed load of 20 kN/m on 0 <= x <= 2;
* a downward distributed load of 10 kN/m on 3 <= x <= 9

Results
-------
A beam representation with the point loads, a shear force diagram and a bending moment diagram are given below.
Note that only the x-coordinate of the point load(s) is marked with a blue arrow (magnitude is not given).

.. figure:: /../../examples/example_1.png

Code
----
.. literalinclude:: /../../examples/example_1.py
