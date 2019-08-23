Beam diagrams
-------------

To state it explicitly once more, the calculation of internal forces for mechanical systems at rest will be based on:

   #. The necessary and sufficient conditions for static equilibrium of a system,
   #. The fact that any arbitrary part of a system is on itself a new system.

So... what if we chose some of the imaginary boundaries that split our system so that they *cut through* a body?
Let's consider a system consisting of a single *beam* [#beam]_ and analyze what happens internally to this body.

.. [#beam] A *beam* will be defined in this context as a long, slender component (i.e. whose length along its main axis is significantly larger than on directions perpendicular to it).

Normal force :math:`N(x)`
*************************

We reserve the name of *normal forces* for those who are perpendicular to a given plane of interest.
In the context of beams (i.e. slender components), we subdivide a body into subsystems by drawing planes perpendicular to its main axis (*x-axis*), as shown in the figure below.
Normal forces are hence perpendicular to these planes, i.e. parallel to the beam's main axis.

The first introductory problem to consider will be a 6 meter long horizontal beam resting on two supports:

  * a roller support at :math:`x=0`
  * a pinned support at :math:`x=3\text{ m}`

.. container:: toggle

    .. container:: header

        **Show/Hide code for generating the image below**

    .. literalinclude:: /../../examples/example_normal0.py
       :lines: 10-24
       :emphasize-lines: 1-5
       :dedent: 4
       :linenos:

.. .. figure:: /_static/placeholder_03.png

.. figure:: /../../examples/example_normal0.png
   :scale: 100 %
   :align: center
   :alt: Beam on two supports with horizontal load

   The beam is held in place by a rolling support at *A* and a pinned support at *B*.
   A normal (tensile) force :math:`F_{1} = 5\text{ kN}` is acting at the right end of the beam.

Let's find the reaction forces first, so we can proceed with our analysis.

.. math::

    \sum{F_x} = 0 \implies F_{Bx} + F_{1} = 0 \implies \underline{F_{Bx} = -5\text{ kN}}\\
    \left.
      \begin{array}{ll}
        \sum{M_A} = 0\\
        \sum{F_z} = 0
      \end{array}
    \right\} \implies \underline{F_A = F_{Bz}} = 0

.. note:: To keep matters simple, the weight of the beam is neglected throughout this analysis.

With the information about the reaction forces at supports *A* and *B*, let's see what happens to the subsystem between the plane 2-2 (located between support *B* and the right end of the beam) and the plane 3-3 (exactly at the right end of the beam, where the load :math:`\mathbf{F_1}` is acting).

.. .. figure:: /_static/placeholder_04.png

.. figure:: /../../examples/example_normal0a.png
   :scale: 100 %
   :align: center
   :alt: Subsystem between sections 2-2 and 3-3 under a horizontal external load.

   Subsystem between planes 2-2 and 3-3, to the right of support *B*.

Let's apply the equilibrium equations to this subsystem.
Since we only have *colinear* forces along the x-axis (we neglect the height of the beam), we write the sum of forces along this direction.
The other equilibrium equations are identically zero (no vertical forces or moments acting on the beam), so they don't add any new information.

.. math::

    \sum{F_x} = 0 \implies F_{1} - N = 0 \implies \underline{N|_{x=x_2} = 5\text{ kN}}

Here we have found the internal normal force :math:`\mathbf{N}` to be equal to 5 kN.
The positive sign corresponds to the standard convention.
The normal force :math:`\mathbf{N}` is defined as positive when it points outwards.
It follows from this that tensile forces are positive and compression forces negative.
The result is the same for any plane located between the support *B* (section 2-2) and the right end of the beam (section 3-3).

Next, let's consider a slightly different subsystem between planes 1-1 and 3-3 and perform the same analysis

.. .. figure:: /_static/placeholder_05.png

.. figure:: /../../examples/example_normal0b.png
   :scale: 100 %
   :align: center
   :alt: Subsystem between sections 1-1 and 3-3 under a horizontal external load.

   Subsystem between planes 1-1 (btw supports *A* and *B*) and 3-3 (beam's right end)

.. math::

    \sum{F_x} = 0 \implies N + F_{Bx} - F_{1} = 0 \implies \underline{N|_{x=x_1} = 0}

The normal force :math:`\mathbf{N}` across the section 1-1 is zero.
Correspondingly, the result is the same for any plane located between supports A (section 1-1) and B (section 3-3).

If we join these last two results, we can reconstruct the normal force :math:`\mathbf{N}` along the full beam span as a function of the :math:`\mathbf{x}` coordinate, which we will predictably call :math:`\mathbf{N(x)}`.
In this simple case, we end up with the following piecewise function:

.. math::

    N(x) = \left\{
      \begin{array}{cl}
         0 \ \ \ & \text{if} \ \  0 \leq x < x_B\\
         5 \text{ kN} \ \ \ & \text{if} \ \  < x_B \leq x < L
      \end{array}
    \right.

.. container:: toggle

    .. container:: header

        **Show/Hide code for generating the image below**

    .. literalinclude:: /../../examples/example_normal1.py
       :lines: 10-14
       :dedent: 4

.. figure:: /../../examples/example_normal1.png
   :scale: 70 %
   :align: center
   :alt: Piecewise function describing the calculated normal force :math:`\mathbf{N(x)}`


Shear force :math:`V(x)` and moment :math:`M(x)`
************************************************

Let's do a similar analysis of the same beam for vertical forces.
Instead of the horizontal force :math:`\mathbf{F_1}`, consider now a vertical force :math:`\mathbf{P_1} = 10\text{ kN}` acting at the beam's right end (plane 3-3).

.. container:: toggle

    .. container:: header

        **Show/Hide code for generating the image below**

    .. literalinclude:: /../../examples/example_shear0.py
       :lines: 10-24
       :emphasize-lines: 1-5
       :dedent: 4
       :linenos:

.. .. figure:: /_static/placeholder_06.png

.. figure:: /../../examples/example_shear0.png
   :scale: 100 %
   :align: center
   :alt: Beam on two supports with vertical load

   The beam is held in place by a rolling support at *A* and a pinned support at *B*.
   A force :math:`P_{1} = 10\text{ kN}` directed upwards is acting at the right end of the beam.

In the same way as before, we start by finding the reaction forces at the supports *A* and *B*.

.. math::

    \sum{F_x} = 0 \implies \underline{F_{Bx} = 0}\\
    \sum{M_A} = 0 \implies F_{Bz} = -\cfrac{\mathbf{P_1}L}{d} = -20 \text{ kN}\\
    \sum{F_z} = 0 \implies F_A = \cfrac{\mathbf{P_1}(L-d)}{d} = 10 \text{ kN}

where :math:`L=6\text{ m}` is the length of the beam, and :math:`d=3\text{ m}` is the distance between supports *A* and *B*.

Next, we draw a free body diagram of the beam section comprised between planes 2-2 and 3-3, and do a balance of forces and moments once more.

.. .. figure:: /_static/placeholder_07.png

.. figure:: /../../examples/example_shear0a.png
   :scale: 100 %
   :align: center
   :alt: Subsystem between sections 2-2 and 3-3 under a vertical external load.

   Subsystem between planes 2-2 and 3-3, to the right of support *B*.

.. math::

    \sum{F_z} = 0 \implies \mathbf{P_1} - V = 0 \implies V = 10 \text{ kN}\\
    \sum{M} = 0 \implies M(x) - \mathbf{P_1} (x-L) = 0 \implies M(x) = \mathbf{P_1} (x-L)

The vertical plane 2-2, corresponds to :math:`x=4\text{ m}`, hence 

   - :math:`V|_{2-2} = V(x)|_{x=4\text{ m}} = \underline{10 \text{ kN}}`, and
   - :math:`M|_{2-2} = M(x)|_{x=4\text{ m}} = \underline{-20 \text{ kN·m}}`.

The negative value of :math:`M(x)|_{x=4\text{ m}}` means that the actual moment acting on the left side of that beam section is *opposite to the arrow drawn in the figure above* (i.e. clockwise instead of counterclockwise).

.. note::
   The sign convention we follow is shown in the figure below:

      * A positive normal force *N* contributes to stretching (elongating) of the beam.
      * A positive shear force *V* points upwards (z+) at the right side of the beam (x+), and downwards (z-) at the left side of the beam (x-).
      * A positive bending moment causes a contributes to stretch on the upper side of the beam and compression on its lower side.

   .. figure:: /../../examples/sign_convention.png
      :scale: 80 %
      :align: center
      :alt: Subsystem between sections 1-1 and 3-3 under a vertical external load.

      Sign convention used for the beam diagrams: the arrow directions correspond to positive values.




Let's calculate now the shear force and bending moment at the vertical plane 1-1.
To that end, we will consider the beam section between planes 1-1 and 2-2, as shown in the figure below.

.. .. figure:: /_static/placeholder_08.png

.. figure:: /../../examples/example_shear0b.png
   :scale: 100 %
   :align: center
   :alt: Subsystem between sections 1-1 and 3-3 under a vertical external load.

   Subsystem between planes 1-1 (btw supports *A* and *B*) and 3-3 (beam's right end)

The equations for sum of forces and sum of moments become then:

.. math::

    \begin{array}{rl}
      \mathbf{\sum{F_z}} = -V_{1-1} + F_{Bz} + V_{2-2} &= 0 \\ 
       -V_{1-1} + (-20 \text{ kN}) + 10 \text{ kN} &= 0 \\ 
       V_{1-1} &= \underline{-10 \text{ kN}}
    \end{array}\\
    \\
    \begin{array}{rrl}
      & \mathbf{\sum{M}} = M_{1-1} + F_{Bz}(d-x) - V_{2-2}(4\text{ m}-x) &= 0 \\ 
      & M_{1-1} + 20\text{ kN}(3\text{ m}-x) - 10 \text{ kN}(4\text{ m}-x) &= 0\\ 
      \text{since } x|_{1-1}=2\text{ m} \implies & M_{1-1} + 20\text{ kN}(3\text{ m}-2\text{ m}) - 10 \text{ kN}(6\text{ m}-2\text{ m}) &= 0\\
      & M_{1-1} &= \underline{-20 \text{ kN·m}}
    \end{array}
    
.. tip::
   This result would (of course) have been the same if our free-body diagram had included the whole beam to the right of the plane 1-1.
   The same is true for a free-body of the left side of the beam.
   In order to make sure you will understand the next section, I suggest you **stop reading for a moment and try to verify this**.

As an exercise, you can follow this procedure and calculate the general result for an arbitrary x-coordinate.
You should obtain a function like the one shown in the image below.

.. container:: toggle

    .. container:: header

        **Show/Hide code for generating the image below**

    .. literalinclude:: /../../examples/example_shear1.py
       :lines: 11-17
       :dedent: 4

.. figure:: /../../examples/example_shear1.png
   :scale: 70 %
   :align: center
   :alt: Piecewise function describing the calculated shear force :math:`\mathbf{V(x)}`
