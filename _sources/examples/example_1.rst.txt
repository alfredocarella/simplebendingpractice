.. _example_1:

Beam with two point loads and two distributed loads
===================================================

This example demonstrates some functionality of the beambending_ package.

.. _beambending: https://github.com/alfredocarella/simplebendingpractice/

Try it in online: |binder| |colab|

.. |binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/alfredocarella/simplebendingpractice/master?filepath=simple_demo.ipynb

.. |colab| image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/alfredocarella/simplebendingpractice/blob/master/simple_demo.ipynb


Specifications
--------------
A beam resting on two supports at x=2 m and x=7 m, with the following applied loads:

* a downward force of 20 kN at x=3 m;
* a force of 10 kN pointing right, also at x=3 m;
* a downward distributed load of 20 kN/m on 0 <= x <= 2 m;
* a downward distributed load of 10 kN/m on 3 m <= x <= 9 m

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
