Simphony-Paraview
=================

A plugin-library for the Simphony framework (http://www.simphony-project.eu/) to provide
visualization support of the CUDS highlevel components.

.. image:: https://travis-ci.org/simphony/simphony-paraview.svg?branch=master
  :target: https://travis-ci.org/simphony/simphony-paraview
  :alt: Build status

.. image:: https://coveralls.io/repos/simphony/simphony-paraview/badge.svg?branch=master
  :target: https://coveralls.io/r/simphony/simphony-paraview?branch=master
  :alt: Test coverage

.. image:: https://readthedocs.org/projects/simphony-paraview/badge/?version=master
  :target: https://readthedocs.org/projects/simphony-paraview/?badge=master
  :alt: Documentation Status

Repository
----------

Simphony-paraview is hosted on github: https://github.com/simphony/simphony-paraview

Requirements
------------

- paraview >= 3.14.1
- simphony >= 0.2.0

Optional requirements
~~~~~~~~~~~~~~~~~~~~~

To support the documentation built you need the following packages:

- sphinx >= 1.2.3
- sectiondoc commit 8a0c2be, https://github.com/enthought/sectiondoc
- mock

Alternative running :command:`pip install -r doc_requirements` should install the
minimum necessary components for the documentation built.

Installation
------------

The package requires python 2.7.x, installation is based on setuptools::

  # build and install
  python setup.py install

or::

  # build for in-place development
  python setup.py develop

Testing
-------

To run the full test-suite run::

  python -m unittest discover

Documentation
-------------

To build the documentation in the doc/build directory run::

  python setup.py build_sphinx

.. note::

  - One can use the --help option with a setup.py command
    to see all available options.
  - The documentation will be saved in the ``./build`` directory.

Usage
-----

After installation the user should be able to import the ``paraview`` visualization plugin module by::

  from simphony.visualization import paraview_tools
  paraview_tools.show(cuds)


Directory structure
-------------------

There are four subpackages:

- simphony-paraview -- Main package code.
- examples -- Holds examples of visualizing simphony objects with simphony-paraview.
- doc -- Documentation related files:

  - source -- Sphinx rst source files
  - build -- Documentation build directory, if documentation has been generated
    using the ``make`` script in the ``doc`` directory.
