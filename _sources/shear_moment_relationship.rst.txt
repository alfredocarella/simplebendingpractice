Relationship between shear force and bending moment
---------------------------------------------------
The analysis in the section above was restricted to point loads in order to keep it simple.
However, it applies universally for distributed loads as well, as we are going to see next.

It may not be obvious at first sight, but the functions corresponding to shear force :math:`\mathbf{V(x)}` and bending moment :math:`\mathbf{M(x)}` are intimately correlated (i.e. you can use one of them for calculating the other one).
We are going to prove this by performing the same analysis explained above to a differential beam segment of length :math:`\Delta x`.

By this point, our analysis methodology should be clear. It consists of the following steps:

   #. Choosing an arbitrary sector of a beam.
   #. Drawing a free-body diagram of the partition.
   #. Applying Newton's first law to the free-body diagram.

.. #. Calculating the (external) reaction forces from the supports. <-- is actually step 1>
  
Let's consider an arbitrarily loaded beam as shown in the figure below, where :math:`\mathbf{P_z}(x)` is an arbitrarily distributed load applied to the beam.

.. .. figure:: /_static/placeholder_09.pngXXXXX

.. figure:: /../../examples/example_distributed0.png
   :scale: 100 %
   :align: center
   :alt: Simply supported beam with an arbitrarily distributed load

   Generic problem consisting of a beam under an arbitrarily distributed load :math:`\mathbf{P_z}(x)`

Let's zoom-in and draw a free-body diagram of a given beam segment :math:`[x_0 \leq x \leq x_0+\Delta x]`.

.. .. figure:: /_static/placeholder_10.png

.. figure:: /../../examples/example_distributed1.png
   :scale: 100 %
   :align: center
   :alt: Free body diagram of a differential segment of the beam

   Free body diagram of a differential segment of the beam

The equilibrium of vertical forces yields then the following:

.. math::

    \begin{array}{rrl}
      & \mathbf{\sum{F_z}} &= 0 \\
      & V(x + \Delta x) -V(x) + \overline{\mathbf{P_z}}(x) \Delta x &= 0 \\
      & \cfrac{V(x + \Delta x) -V(x)}{\Delta x} &= -\overline{\mathbf{P_z}}(x) \\
      \lim_{\Delta x \to 0} & \boxed{\cfrac{dV(x)}{dx} = -\mathbf{P_z}(x)}
    \end{array}

which in words means that the rate of change of the shear force is equal to (minus) the value of the distributed load acting on a given x-coordinate.

Note that in the expression above, :math:`\overline{\mathbf{P_z}}(x)` represents the average value of :math:`\mathbf{P_z}(x)` in the given interval.
As :math:`\Delta x` goes to zero, :math:`\overline{\mathbf{P_z}}(x)` converges to :math:`\mathbf{P_z}(x)`.

The equilibrium of moments can be written as:

.. math::

    \begin{array}{rrl}
      & \mathbf{\sum M|_{x + \Delta x}} &= 0 \\
      & M(x + \Delta x) -M(x) - V(x) \Delta x + (\overline{\mathbf{P_z}}(x) \Delta x \cdot \frac{\Delta x}{2}) &= 0 \\
      & \cfrac{M(x + \Delta x) -M(x)}{\Delta x} + \underbrace{(\overline{\mathbf{P_z}}(x) \Delta x \cdot \frac{\Delta x}{2})}_{\Delta x^2\to 0} &= V(x) \\
      \lim_{\Delta x \to 0} & \boxed{\cfrac{dM(x)}{dx} = V(x)}
    \end{array}

which presents explicitly the relationship between :math:`M(x)` and :math:`V(x)`: the rate of change of the bending moment at a given point is equal to the shear force at that point.

Ok, that was it. For a worked example, take a look at the next section: :ref:`example_1`.
