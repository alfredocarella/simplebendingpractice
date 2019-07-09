# -*- coding: utf-8 -*-
"""Setup file for simplebending package

Developer install
-----------------
Run following command in Anaconda prompt/terminal:
    pip install -e .
"""
from setuptools import setup


setup(name='beambending',  # name of package on import
      version='1.0',  # package version
      description='Educational package for visualizing shear forces and bending moments on 1-D beams',  # brief description
      license='cc-by-4.0',  # licensing
      long_description=open('README.md').read(),
      url='https://github.com/alfredocarella/simplebendingpractice',  # git repo url
      author='Alfredo Carella',  # author(s)
      author_email='alfcar@oslomet.no',  # email
      packages=['beambending'],  # main package
      install_requires=[  # dependencies
        'matplotlib',  # for plotting
        'numpy',  # for numerical calculations
        'numpydoc',  # numpy-style docstrings for sphinx
        'pytest',  # for testing
        'pytest-cov',  # for calculating coverage
        'sphinx',  # generating documentation
        'sphinx_rtd_theme',  # docs theme
        'sympy'  # for analytical integration
      ],
      zip_safe=True)  # package can be installed from zip file
