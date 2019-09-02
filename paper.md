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
nocite: | 
  @beamguru, @structuralbeam, @skyciv, @mechanicalc, @engineersedge, @webstructural, @beamcalculatoronline, @steelbeamcalculator
---

# Summary
BeamBending is _both_ an educational module _and_ a Python package, based mainly on @Hunter2007, @oliphant2006guide and @sympy2017 It is intended to serve as a teaching aid during a first course in Statics.
This module aims to enhance clarity and provide visual hands-on examples while introducing the concepts of:

* stresses on slender _one-dimensional_ solids (i.e. beams)
* normal force, shear force, and bending moment diagrams

The [package documentation](https://alfredocarella.github.io/simplebendingpractice/) includes a simple (but still rigorous enough) explanation of the background theory, inspired in @Beer2017 and @Bell2015.
It is assumed that the students understand static equilibrium of flat rigid bodies, but a short recap is provided.
Code snippets that reproduce the theory examples are presented next to each result.

The package can be used by

* teachers who want to automatically create problem sets with their solutions (easily scriptable, _random-problem-generator friendly_);
* students who want to verify their solutions to introductory problem sets;
* students who like to play with example problems and receive immediate visual feedback (i.e. about how simple modifications to imposed loads affect the resulting reaction forces and internal stresses).

The `beambending` package is ready for installation using `pip` or can be tested online using the provided [Jupyter notebook](https://mybinder.org/v2/gh/alfredocarella/simplebendingpractice/master?filepath=simple_demo.ipynb).


# Statement of Need
Statics courses in undergraduate engineering programs are sometimes taught before the knowledge of the relevant mathematical tools (i.e. simple calculus and linear vector algebra) is fully mature.
Introducing a topic that resembles the mindset of calculus and employs an unintuitive standard sign convention, on top of a wobbly mathematical foundation, makes it fairly common for students to get lost in the calculations.
<!-- This becomes an additional challenge for students in their first encounter with the topic of shear forces and bending moments in beams. -->

This package/module aims to bridge this gap and simplify students' first contact with this challenging new topic by working on two fronts simultaneously:

* Explain the [background theory](https://alfredocarella.github.io/simplebendingpractice/background.html) from a simple example with focus on connecting the mathematical description with the physical beam model (`beambending` code snippets are interleaved to illustrate how the package works).
* Provide a temporary scaffolding that helps to establish an immediate visual association between beam load states and internal stresses.

Several online tools with similar functionality are currently available, such as Beam Guru (2019), Structural Beam Deflection and Stress Calculators (2019), SkyCiv Beam (2017), MechaniCalc (2019), Engineers Edge (2019), WebStructural (2019), Beam Calculator Online (2019), and Steel Beam Calculator (2019).
Most of them expose only a graphical user interface to the user, eliminating the need to write any code; roughly half of the surveyed tools are free while others charge monthly subscriptions, and only a few include a theoretical module or present to the user a detailed solution procedure for the problems.
This feature comparison is presented in Table 1.

![](https://github.com/alfredocarella/simplebendingpractice/raw/master/tool_comparison_table.png)

There are three main differences between the ```beambending``` package and the rest of the reviewed tools:

* Arbitrary distributed load functions are accepted (as long as sympy can parse them), i.e. they are not restricted to constants or linear functions.
* The package (and parts of it) can be called from regular Python code, which makes it easy to automatically generate problem sets with solutions.
* It is not only free but also completely open-source.


# Functionality and Usage
A typical use case of the `beambending` package always involves creating an instance of the `Beam` class. The class constructor takes an optional _length_ argument, which defaults to 10 in case no argument is provided.

```python
from beambending import Beam
beam = Beam(9)  # Initialize a Beam object of length 9m
```

After a `Beam` object is created, the properties corresponding to the x-coordinates of the pinned and rolling supports must be defined.

```python
beam.pinned_support = 2    # x-coordinate of the pinned support
beam.rolling_support = 7  # x-coordinate of the rolling support
```

Note that the Beam class currently supports only statically determined beams with (exactly) one pinned and one roller support.

Each load applied to the beam requires an instance of one of the load classes `DistributedLoadH`, `DistributedLoadV`, `PointLoadH`, or `PointLoadV`.
The load classes are simply _namedtuples_, and make the resulting scripts easier to read by making the user's intention explicit.
The symbolic variable `x`, also defined by the module, is used for defining variable distributed loads.

```python
from beambending import DistributedLoadV, PointLoadH, PointLoadV, x
```

The loads can be applied to the `Beam` by passing an iterable (list or tuple) to the method `add_loads`.

```python
beam.add_loads((
                # 10kN pointing right, at x=3m
                PointLoadH(10, 3),
                # 20kN downwards, at x=3m
                PointLoadV(-20, 3),
                # 10 kN/m, downward, for 3m <= x <= 9m
                DistributedLoadV(-10, (3, 9)),
                # Variable load, for 0m <= x <= 2m
                DistributedLoadV(-20 + x**2, (0, 2)),
            ))
```

After the problem is fully defined (beam length + placement of supports + loads), the `plot` method can be invoked to plot a sketch of the loaded beam together with its corresponding load diagrams (normal force, shear force and bending moment).

```python
fig = beam.plot()
```

The `plot` method is actually a wrapper that combines these four methods: `plot_beam_diagram`, `plot_normal_force`, `plot_shear_force` and `plot_bending_moment` into a single A4-sized printer-friendly plot.

## Example
The following example, provided within the [package documentation](https://alfredocarella.github.io/simplebendingpractice/reference.html), summarizes the explanation above.
The output is shown in Figure 1.

```python
from beambending import Beam, DistributedLoadV, PointLoadH, PointLoadV, x
beam = Beam(9)
beam.pinned_support = 2
beam.rolling_support = 7
beam.add_loads((
                PointLoadH(10, 3),
                PointLoadV(-20, 3),
                DistributedLoadV(-10, (3, 9)),
                DistributedLoadV(-20 + x**2, (0, 2)),
            ))
fig = beam.plot()
```

![Output corresponding to the example code](https://github.com/alfredocarella/simplebendingpractice/raw/master/examples/example_1_62pct.png)


# Recent Uses
The `beambending` package was developed as a teaching aid for the *Statics* course in the Autumn 2019 semester at OsloMet - Oslo Metropolitan University.
Beta versions were tried and commented by students during the Autumn 2018 semester, but the effectiveness of the tool has not been tested with large groups of students yet.


# References
