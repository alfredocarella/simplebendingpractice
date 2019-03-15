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

The vertical plane 2-2, corresponds to :math:`x=4`, hence 
   - :math:`V|_{2-2} = V(x)|_{x=4} = \underline{10 \text{kN}}`, and
   - :math:`M|_{2-2} = M(x)|_{x=4} = \underline{20 \text{kNm}}`.

Let's calculate now the shear force and bending moment at the vertical plane 1-1.
To that end, we will consider the beam section between planes 1-1 and 2-2, as shown in the figure below.

.. todo::
   Clarify the sign convention:
      - Explain that :math:`V_{2-2}` and :math:`M_{2-2}` to the right of section 1-2 are (equal and opposite) reactions to :math:`V_{2-2}` and :math:`M_{2-2}` to the left of section 2-3.

.. figure:: /_static/placeholder_08.png
   :scale: 100 %
   :align: center
   :alt: Insert alternative text here

   **PLACEHOLDER FIG:** Insert caption here

The equations for sum of forces and sum of moments become then:

.. math::

    \begin{array}{rl}
      \mathbf{\sum{F_z}} = -V_{1-1} + F_{Bz} + V_{2-2} &= 0 \\ 
       -V_{1-1} + (-20 \text{kN}) + 10 \text{kN} &= 0 \\ 
       V_{1-1} &= \underline{-10 \text{kN}}
    \end{array}\\
    \\
    \begin{array}{rrl}
      & \mathbf{\sum{M}} = M_{1-1} + F_{Bz}(d-x) - V_{2-2}(4\text{m}-x) &= 0 \\ 
      & M_{1-1} + 20\text{kN}(3\text{m}-x) - 10 \text{kN}(4\text{m}-x) &= 0\\ 
      \text{since } x|_{1-1}=2\text{m} \implies & M_{1-1} + 20\text{kN}(3\text{m}-2\text{m}) - 10 \text{kN}(4\text{m}-2\text{m}) &= 0\\
      & M_{1-1} &= \underline{0}
    \end{array}
    
.. todo::

   Add plot for function and code for Python example using the *beambending* package.

.. note::
   This result would (of course) have been the same if our free-body diagram had included the whole beam to the right of the plane 1-1.
   The same is true for a free-body of the left side of the beam.
   In order to make sure you will understand the next section, I suggest you **stop reading for a moment and try to verify this**.


Relationship between shear force :math:`\mathbf{V(x)}` and bending moment :math:`\mathbf{M(x)}`
-----------------------------------------------------------------------------------------------
 The analysis in the section above was restricted to point loads in order to keep it simple.
 However, it applies universally for distributed loads as well, as we are going to see next.

It may not be obvious at first sight, but the functions corresponding to shear force :math:`\mathbf{V(x)}` and bending moment :math:`\mathbf{M(x)}` are intimately correlated (i.e. you can use one of them for calculating the other one).
We are going to prove this by performing the same analysis explained above to a differential beam segment of length :math:`\Delta x`.

By this point, our analysis methodology should be clear. It consists of three steps:
   #. Choosing an arbitrary sector of a beam.
   #. Drawing a free-body diagram of the partition.
   #. Applying Newton's first law to the free-body diagram.

.. #. Calculating the (external) reaction forces from the supports. <-- is actually step 1>
  
Let's consider an arbitrarily loaded beam as shown in the figure below.

.. figure:: /_static/placeholder_09.png
   :scale: 100 %
   :align: center
   :alt: Insert alternative text here

   **PLACEHOLDER FIG:** Insert caption here

Let's draw a free-body diagram of a given beam segment :math:`[x_0 \leq x \leq x_0+\Delta x]`, where :math:`\mathbf{P_z}(x)` is a distributed load applied to the beam.

.. figure:: /_static/placeholder_10.png
   :scale: 100 %
   :align: center
   :alt: Insert alternative text here

   **PLACEHOLDER FIG:** Insert caption here

The equilibrium of vertical forces yields the following:

.. math::

    \begin{array}{rrl}
      & \mathbf{\sum{F_z}} &= 0 \\
      & V(x + \Delta x) -V(x) + \mathbf{P_z}(x) \Delta x &= 0 \\
      & \cfrac{V(x + \Delta x) -V(x)}{\Delta x} &= -\mathbf{P_z}(x) \\
      \lim_{\Delta x \to 0} & \boxed{\cfrac{dV(x)}{dx} = -\mathbf{P_z}(x)}
    \end{array}

which in words means that the rate of change of the shear force is equal to (minus) the value of the distributed load acting on a given x-coordinate.

The equilibrium of moments can be written as:

.. math::

    \begin{array}{rrl}
      & \mathbf{\sum M|_{x + \Delta x}} &= 0 \\
      & M(x + \Delta x) -M(x) - V(x) \Delta x + (\mathbf{P_z}(x) \Delta x \cdot \frac{\Delta x}{2}) &= 0 \\
      & \cfrac{M(x + \Delta x) -M(x)}{\Delta x} + \underbrace{(\mathbf{P_z}(x) \Delta x \cdot \frac{\Delta x}{2})}_{\Delta x^2\to 0} &= V(x) \\
      \lim_{\Delta x \to 0} & \boxed{\cfrac{dM(x)}{dx} = V(x)}
    \end{array}

which presents explicitly the relationship between :math:`M(x)` and :math:`V(x)`: the rate of change of the bending moment at a given point is equal to the shear force at that point.

.. todo::

   Replace the figure below by a Python example using the **beambending** package

.. figure:: /_static/placeholder_12.png
   :scale: 100 %
   :align: center
   :alt: Insert alternative text here

   **PLACEHOLDER FIG:** Insert caption here




