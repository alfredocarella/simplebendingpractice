# BeamBending: a teaching aid for 1-D shear-force and bending-moment diagrams

[![Version](https://img.shields.io/badge/version-1.1.1-blue.svg)](https://github.com/alfredocarella/simplebendingpractice/releases/tag/1.1.1)
[![License](https://img.shields.io/badge/license-CC--BY%204.0-lightgrey.svg)](https://github.com/alfredocarella/simplebendingpractice/raw/master/LICENSE)
[![DOI](https://jose.theoj.org/papers/10.21105/jose.00065/status.svg)](https://doi.org/10.21105/jose.00065)
[![Build Status](https://travis-ci.com/alfredocarella/simplebendingpractice.svg?branch=master)](https://travis-ci.com/alfredocarella/simplebendingpractice)
[![Documentation Status](https://readthedocs.org/projects/simplebendingpractice/badge/?version=latest)](https://simplebendingpractice.readthedocs.io/en/latest/?badge=latest)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/alfredocarella/simplebendingpractice/master?filepath=simple_demo.ipynb)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredocarella/simplebendingpractice/blob/master/simple_demo.ipynb)

BeamBending is _both_ an educational module _and_ a Python package, intended to serve as a teaching aid during a first course in _Statics_.
The aim of this module is to enhance clarity and provide visual hands-on examples while introducing the concepts of:
* stresses on slender _one-dimensional_ solids (i.e. beams)
* normal force, shear force and bending moment diagrams

The [package documentation](https://alfredocarella.github.io/simplebendingpractice/) includes a simplified (but still rigorous enough) explanation of the background theory, inspired in [@Beer2017] and [@Bell2015].
It is assumed that the students understand static equilibrium of flat rigid bodies, but a short recap is provided.
Code snippets that reproduce the theory examples are presented next to each result.

The package can be used by
* teachers who want to automatically create problem sets with their solutions (easily scriptable, _random-problem-generator friendly_);
* students who want to verify their solutions to introductory problem sets;
* students who like to play with example problems and receive immediate visual feedback about how simple modifications to imposed loads affect the resulting reaction forces and internal stresses.

The materials are distributed publicly and openly under a Creative Commons Attribution license, [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)


## Cite as:

Carella, (2019). BeamBending: a teaching aid for 1-D shear force and bending moment diagrams. Journal of Open Source Education, 2(19), 65, https://doi.org/10.21105/jose.00065


## Statement of Need

Statics courses in undergraduate engineering programs are sometimes taught before the knowledge of the relevant mathematical tools (i.e. simple calculus and linear vector algebra) is fully mature.
Introducing a topic that resembles the mindset of calculus and employs an unintuitive standard sign convention, on top of a wobbly mathematical foundation, makes it fairly common for students to get lost in the calculations.

This package/module aims to bridge this gap and simplify students' first contact with this challenging new topic by working on two fronts simultaneously:
1. Explain the [background theory](https://alfredocarella.github.io/simplebendingpractice/background.html) from a simple example with focus on connecting the mathematical description with the physical beam model (`beambending` code snippets are interleaved in order to illustrate how the package works).
2. Provide a temporary scaffolding that helps to establish an immediate visual association between beam load states and internal stresses.


## Functionality and Usage

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

Note that the Beam class currently supports only statically determined beams with _exactly_ one pinned and one roller support.

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

After the problem is fully defined (beam length + placement of supports + loads), the `plot` method can be invoked to plot a sketch of the loaded beam together with its corresponding load diagrams (normal force, shear force and bending moment).

```python
fig = beam.plot()
```

The `plot` method is actually a wrapper that combines these four methods: `plot_beam_diagram`, `plot_normal_force`, `plot_shear_force` and `plot_bending_moment` into a single A4-sized printer-friendly plot.

The script above produces the following figure:
![Output corresponding to the example code above](https://github.com/alfredocarella/simplebendingpractice/raw/master/examples/example_1.png)

You can read about this example in context in the [documentation](https://alfredocarella.github.io/simplebendingpractice/examples/example_1.html), or try it in a Jupyter notebook hosted online: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/alfredocarella/simplebendingpractice/master?filepath=simple_demo.ipynb) [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredocarella/simplebendingpractice/blob/master/simple_demo.ipynb)

For more sophisticated applications, like automatic problem generation, you should read the [package documentation](https://alfredocarella.github.io/simplebendingpractice/reference.html).



## Installing the package

If you want to install the `beambending` package, you run this one-liner:

```shell
pip install --user beambending
```

> **NOTE**: You need Python 3 to install this package (you may need to write `pip3` instead of `pip`).

The library dependencies are listed in the file `requirements.txt`, but you only need to look at them if you clone the repository.
If you install the package via `pip`, the listed dependencies should be installed automatically.


## How to contribute to BeamBending

The guidelines for contributing are specified [here](https://github.com/alfredocarella/simplebendingpractice/blob/master/CONTRIBUTING.md).

## Copyright and License

(c) 2018 Alfredo R. Carella. All content is under Creative Commons Attribution [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode.txt).

You are welcome to re-use this content in any way.
