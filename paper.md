---
title: 'BeamBending: a teaching aid for 1-D shear force and bending moment diagrams'
tags:
- bending moment diagram
- shear force diagram
- normal force diagram
- statics
- mechanics
- Python
authors:
- name: Alfredo R. Carella
  orcid: 0000-0001-8340-3427
  affiliation: 1
affiliations:
- name: OsloMet - Oslo Metropolitan University
  index: 1
date: 8 July 2019
bibliography: paper.bib
---

# Summary
BeamBending is _both_ an educational module _and_ a Python package, intended to serve as a teaching aid during a first course in _Statics_.
The aim of this module is to enhance clarity and provide visual hands-on examples while introducing the concepts of:
* stresses on slender _one-dimensional_ solids (i.e. beams)
* normal force, shear force and bending moment diagrams

The [package documentation](https://alfredocarella.github.io/simplebendingpractice/) includes a simple (but still rigorous) explanation of the background theory, inspired in [@Bell2015].
It is assumed that the students understand static equilibrium of flat rigid bodies, but a short recap is provided.
Code snippets that reproduce the theory examples are presented next to each result.

The package can be used by
* teachers who want to automatically create problem sets with their solutions (easily scriptable, _random-problem-generator friendly_);
* students who want to verify their solutions to introductory problem sets;
* students who like to play with example problems and receive immediate visual feedback about how simple modifications to imposed loads affect the resulting reaction forces and internal stresses.

The `beambending` package is ready for installation using `pip`, or can be tested online using the provided [Jupyter notebook](https://mybinder.org/v2/gh/alfredocarella/simplebendingpractice/master?filepath=simple_demo.ipynb).


# Statement of Need
Statics courses in undergraduate engineering programs are sometimes taught before the knowledge of the relevant mathematical tools (i.e. simple calculus and linear vector algebra) is fully mature.
Introducing a topic that resembles the mindset of calculus and employs a little intuitive standard sign convention, on top of a wobbly mathematical foundation, makes it fairly common for students to get lost in the calculations.
<!-- This becomes an additional challenge for students in their first encounter with the topic of shear forces and bending moments in beams. -->

This package/module aims to bridge this gap and simplify students' first contact with this challenging new topic by working on two fronts simultaneously:
1. Explain the [background theory](https://alfredocarella.github.io/simplebendingpractice/background.html) from a simple example with focus on connecting the mathematical description with the physical beam model (`beambending` code snippets are interleaved in order to illustrate how the package works).
2. Provide a temporary scaffolding that helps to establish an immediate visual association between beam load states and internal stresses.


# Functionality and Usage
A typical use case of the `beambending` package always involves creating an instance of the `Beam` class. The class constructor takes an optional _length_ argument, which defaults to 10 in case no argument is provided.

```python
from beambending import Beam
beam = Beam(9)  # Initialize a Beam object of length 9m
```

After a `Beam` object is created, the properties corresponding to the x-coordinates of the fixed and rolling supports must be defined.

```python
beam.fixed_support = 2    # x-coordinate of the fixed support
beam.rolling_support = 7  # x-coordinate of the rolling support
```

Each load applied to the beam requires an instance of one of the load classes `DistributedLoadH`, `DistributedLoadV`, `PointLoadH`, or `PointLoadV`.
The load classes are simply _namedtuples_, and make the resulting scripts easier to read by making the user's intention explicit.
The symbolic variable `x`, also defined by the module, is used for defining variable distributed loads.

```python
from beambending import DistributedLoadV, PointLoadH, PointLoadV, x
```

The loads can be applied to the `Beam` by passing an iterable (list or tuple) to the method `add_loads`.

```python
beam.add_loads((
                PointLoadH(10, 3),  # 10kN pointing right, at x=3m
                PointLoadV(-20, 3),  # 20kN downwards, at x=3m
                DistributedLoadV(-10, (3, 9)),  # 10 kN/m, downward, for 3m <= x <= 9m
                DistributedLoadV(-20 + x**2, (0, 2)),  # variable load, for 0m <= x <= 2m
            ))
```

After the problem is fully defined (beam length + placement of supports + loads), the `plot` method can me invoked to plot a sketch of the loaded beam together with its corresponding load diagrams (normal force, shear force and bending moment).

```python
fig = beam.plot()
```

The `plot` method is actually a wrapper that combines these four methods: `plot_beam_diagram`, `plot_normal_force`, `plot_shear_force` and `plot_bending_moment` into a single A4-sized printer-friendly plot.

## Example
The following example, provided within the [package documentation](https://alfredocarella.github.io/simplebendingpractice/reference.html), summarizes the explanation above.

### Input
```python
from beambending import Beam, DistributedLoadV, PointLoadH, PointLoadV, x
beam = Beam(9)  # Initialize a Beam object of length 9m
beam.fixed_support = 2    # x-coordinate of the fixed support
beam.rolling_support = 7  # x-coordinate of the rolling support
beam.add_loads((
                PointLoadH(10, 3),  # 10kN pointing right, at x=3m
                PointLoadV(-20, 3),  # 20kN downwards, at x=3m
                DistributedLoadV(-10, (3, 9)),  # 10 kN/m, downwards, for 3m <= x <= 9m
                DistributedLoadV(-20 + x**2, (0, 2)),  # variable load, for 0m <= x <= 2m
            ))
fig = beam.plot()
```

### Output
The script above produces the following Matplotlib figure:
![Output corresponding to the example code above](.\examples\example_1.png)


# Recent Uses
I developed `beambending` for using it in my *Statics* course in the Autumn 2019 semester at OsloMet - Oslo Metropolitan University.
Beta versions were tried and commented by students during the Autumn 2018 semester, but the effectiveness of the package has still not been tested with large groups of students.


# References
