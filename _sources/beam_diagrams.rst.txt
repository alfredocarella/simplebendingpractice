Beam diagrams
===========================

In this page we will go through introductory bending theory, as typically covered in an introductory statics course.
We will start by a quick overview of the required knowledge, and then derive our analysis from basic principles.

Background knowledge
--------------------

We have already established that for a body to be at rest, the **vector sum** of all forces :math:`\mathbf{F_i}` and moments :math:`\mathbf{M_i}` acting on it must be zero.

.. math::
   :label: static

   \sum \mathbf{F_i} = 0; \ \ \ \ \ \sum \mathbf{M_i} = 0

.. figure:: /_static/placeholder_01.png
   :scale: 50 %
   :align: center
   :alt: rigid body with forces acting on it (resultant zero)

   **PLACEHOLDER FIG:** A rigid body in equilibrium (i.e. whose sum of both forces and moments equal zero)

Furthermore, for a system to be at rest, each of its components need to be at rest.
This means that Eq. :eq:`static` must be satisfied for each of our system's components.
This is exemplified in the figure below, where according to the action-reaction principle :math:`\mathbf{F_{1C}} = \mathbf{-F_{2C}}`.

.. figure:: /_static/placeholder_02.png
   :scale: 50 %
   :align: center
   :alt: system where the resultant force acting on each one of the rigid bodies is zero

   **PLACEHOLDER FIG:** For a system to be in equilibrium, each of its subsystems **must** be in equilibrium.

So far, we have only considered subsystems consisting of one or more rigid bodies that compose the system.
This means that, so far, each rigid body belonged to *exactly one* subsystem.
However, Eq. :eq:`static` is even more general than that, since it applies to any arbitrary subset of a body.
In the next section, we are going to extract some insights from this.


Internal forces
---------------

To state it explicitly once more, the calculation of internal forces for mechanical systems at rest will be based on:
   #. The necessary and sufficient conditions for static equilibrium of a system, namely Eq. :eq:`static`
   #. The fact that any arbitrary part of a system is on itself a new system.

So... what if we chose some of the imaginary boundaries that split our system so that they *cut through* a body?
Let's consider a system consisting of a single beam, as depicted below, and analyze what happens internally to this body.


Normal force [N(x)]
*******************

We reserve the name of *normal forces* for those who are perpendicular to a given plane of interest.
In the context of beams (i.e. slender components), we subdivide a body into subsystems by drawing planes perpendicular to its main axis, as shown in the figure below.
Normal forces are hence perpendicular to these planes, i.e. parallel to the beam's main axis.

.. figure:: /_static/placeholder_03.png
   :scale: 100 %
   :align: center
   :alt: Beam on two supports

   **PLACEHOLDER FIG:** The beam is held in place by a rolling support at *A* and a fixed support at *B*.
   A normal (tensile) force :math:`F_{1} = 5\text{kN}` is acting at the right end of the beam.

Let's find the reaction forces first, so we can proceed with our analysis.

.. math::

    \sum{F_x} = 0 \implies F_{Bx} + F_{1} = 0 \implies \underline{F_{Bx} = -5\text{kN}}\\
    \left.
      \begin{array}{ll}
        \sum{M_A} = 0\\
        \sum{F_z} = 0
      \end{array}
    \right\} \implies \underline{F_A = F_{Bz}} = 0

With the information about the reaction forces at supports *A* and *B*, let's see what happens to the subsystem between the plane 2-2 (located between support *B* and the right end of the beam) and the plane 3-3 (exactly at the right end of the beam, where the load :math:`\mathbf{F_1}` is acting).

.. figure:: /_static/placeholder_04.png
   :scale: 100 %
   :align: center
   :alt: Subsystem between sections 2-2 and 3-3

   **PLACEHOLDER FIG:** Subsystem between planes 2-2 and 3-3, to the right of support *B*.
   Note that the weight of the beam is always neglected.

Let's apply the equilibrium equations to this subsystem.
Since we only have *colinear* forces along the x-axis (we neglect the height of the beam), we write the sum of forces along this direction.
The other equilibrium equations are identically zero (no vertical forces or moments acting on the beam), so they don't add any new information.

.. math::

    \sum{F_x} = 0 \implies N - F_{1} = 0 \implies \underline{N|_{x=x_2} = 5\text{kN}}

Here we have found the internal normal force :math:`\mathbf{N}` to be equal to 5kN.
The positive sign corresponds to our choice of the orientation of :math:`\mathbf{N}`.
It is customary to define :math:`\mathbf{N}` as positive when pointing outwards.
It follows from this that tensile forces are positive and compression forces negative.
The result would be the same for any choice of the line 2-2 between the support *B* and the right end of the beam.

Next, let's consider an extended subsystem between planes 1-1 and 3-3 and perform the same analysis

.. figure:: /_static/placeholder_05.png
   :scale: 100 %
   :align: center
   :alt: Subsystem between sections 1-1 and 3-3

   **PLACEHOLDER FIG:** Subsystem between planes 1-1 (btw supports *A* and *B*) and 3-3 (beam's right end)

.. math::

    \sum{F_x} = 0 \implies N + F_{Bx} - F_{1} = 0 \implies \underline{N|_{x=x_1} = 0}

If we join these two results, we can plot the *internal* normal force :math:`\mathbf{N}` as a function of the :math:`\mathbf{x}` coordinate, as :math:`\mathbf{N(x)}`.
In this simple case, what we end up with is the following piecewise function:

.. math::

    N(x) = \left\{
      \begin{array}{cl}
         0 \ \ \ & \text{if} \ \  0 \leq x < x_B\\
         -5 \text{kN} \ \ \ & \text{if} \ \  < x_B \leq x < L
      \end{array}
    \right.

.. todo::

   Add plot for function and code for Python example using the *beambending* package.


Shear force [V(x)] and moment [M(X)]
************************************

Let's do a similar analysis of the same beam for vertical forces.
Instead of the horizontal force :math:`\mathbf{F_1}`, consider now a vertical force :math:`\mathbf{P_1} = 10\text{kN}` acting at the beam's right end (plane 3-3).

.. figure:: /_static/placeholder_06.png
   :scale: 100 %
   :align: center
   :alt: Insert alternative text here

   **PLACEHOLDER FIG:** Insert caption here **Distance between 2-2 and 3-3 needs to increase to 2m**

In the same way as before, we start by finding the reaction forces at the supports *A* and *B*.

.. math::

    \sum{F_x} = 0 \implies \underline{F_{Bx} = 0}\\
    \sum{M_A} = 0 \implies F_{Bz} = -\cfrac{\mathbf{P_1}L}{d} = -20 \text{kN}\\
    \sum{F_z} = 0 \implies F_A = \cfrac{\mathbf{P_1}(L-d)}{d} = 10 \text{kN}

where :math:`L=6\text{m}` is the length of the beam, and :math:`d=3\text{m}` is the distance between supports *A* and *B*.

Next, we draw a free body diagram of the beam section comprised between planes 2-2 and 3-3, and apply Eq. :eq:`static` once more.

.. todo::
   Change the distance between planes 2-2 and 3-3- from 1m to 2m. This eliminates periodic decimals and avoids potential confusion between V=10kN and M=10kNm

.. figure:: /_static/placeholder_07.png
   :scale: 100 %
   :align: center
   :alt: Insert alternative text here

   **PLACEHOLDER FIG:** Insert caption here

.. math::

    \sum{F_z} = 0 \implies V + \mathbf{P_1} = 0 \implies V = 10 \text{kN}\\
    \sum{M} = 0 \implies M(x) - \mathbf{P_1} (L-x) = 0 \implies M(x) = \mathbf{P_1} (L-x)

At the plane 2-2, the horizontal coordinate is :math:`x=4`, hence :math:`M|_{2-2} = M(x)|_{x=4} = 20 \text{kNm}`.



.. figure:: /_static/placeholder_08.png
   :scale: 100 %
   :align: center
   :alt: Insert alternative text here

   **PLACEHOLDER FIG:** Insert caption here

.. note::
   We have performed this analysis for point loads, but it applies universally for distributed loads as well.
   More on that in the next section.


Relationship between shear force [V(x)] and bending moment [M(X)]
-----------------------------------------------------------------

It may not be obvious at first sight, but the functions corresponding to shear force :math:`\mathbf{V(x)}` and bending moment :math:`\mathbf{M(x)}` are intimately correlated (i.e. you can calculate one from knowing the other).

By this point, our analysis methodology should be clear. It consists of three simple steps:
   #. Choosing an arbitrary sector of a beam,
   #. Drawing a free body diagram (FBD) of the partition,
   #. Application of Newton's first law to the FBD.

In order to show this, let's consider an arbitrary load situation

.. figure:: /_static/placeholder_09.png
   :scale: 100 %
   :align: center
   :alt: Insert alternative text here

   **PLACEHOLDER FIG:** Insert caption here

.. figure:: /_static/placeholder_10.png
   :scale: 100 %
   :align: center
   :alt: Insert alternative text here

   **PLACEHOLDER FIG:** Insert caption here

.. figure:: /_static/placeholder_11.png
   :scale: 100 %
   :align: center
   :alt: Insert alternative text here

   **PLACEHOLDER FIG:** Insert caption here

.. figure:: /_static/placeholder_12.png
   :scale: 100 %
   :align: center
   :alt: Insert alternative text here

   **PLACEHOLDER FIG:** Insert caption here




