# -*- coding: utf-8 -*-
"""Setup file for simplebending package

Developer install
-----------------
Run following command in Anaconda prompt/terminal:
    pip install -e .
"""
from setuptools import setup


setup(name='beambending',  # name of package on import
      version='1.1.1',  # package version
      description='Educational package for visualizing shear forces and bending moments on 1-D beams',  # brief description
      license='cc-by-4.0',  # licensing
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      url='https://github.com/alfredocarella/simplebendingpractice',  # git repo url
      author='Alfredo Carella',  # author(s)
      author_email='alfredocarella@gmail.com',  # email
      download_url =
      'https://github.com/alfredocarella/simplebendingpractice/archive/1.1.1.tar.gz',    # Link to package release
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
    classifiers=[
      'Development Status :: 4 - Beta',         # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package    
      'Programming Language :: Python :: 3',    #Specify which pyhton versions that you want to support
    ],
      zip_safe=True  # package can be installed from zip file
)