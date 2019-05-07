.. _example_1

Beam with two point loads and two distributed loads
===================================================

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
The figure below shows the load case corresponding to the description above.
The resulting diagrams are respectively:

#. a schematic of the beam and its applied (external) loads [#pointload]_ ,
#. a normal force diagram: :math:`\mathbf{N(x)}`,
#. a shear force diagram :math:`\mathbf{V(x)}`, and
#. a bending moment diagram :math:`\mathbf{M(x)}`.

.. [#pointload] The x-coordinates of the point loads are marked with green arrows, but magnitudes are not displayed in the beam schematic in order to keep the figure clean and simple.

.. figure:: /../../examples/example_1.png

Code
----
.. literalinclude:: /../../examples/example_1.py
