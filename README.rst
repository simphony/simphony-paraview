Simphony-Paraview
=================

A plugin-library for the Simphony framework (http://www.simphony-project.eu/) to provide
visualization support (using http://www.paraview.org/) of the CUDS highlevel components.

.. image:: https://travis-ci.org/simphony/simphony-paraview.svg?branch=master
  :target: https://travis-ci.org/simphony/simphony-paraview
  :alt: Build status

.. image:: http://codecov.io/github/simphony/simphony-paraview/coverage.svg?branch=master
  :target: http://codecov.io/github/simphony/simphony-paraview?branch=master
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


``simphony-paraview`` is known to work with paraview 3.14.1 (official)
and paraview 4.1.0 (paraviewopenfoam) on Ubuntu 12.04
(precise). Installation instructions are provided below.

Paraview 3.14.1
~~~~~~~~~~~~~~~

::

  sudo apt-get install paraview

ParaviewOpenFoam 4.1.0
~~~~~~~~~~~~~~~~~~~~~~

::

  sudo sh -c "echo deb http://www.openfoam.org/download/ubuntu precise main > /etc/apt/sources.list.d/openfoam.list"
  sudo apt-get update
  sudo apt-get paraviewopenfoam410



Optional requirements
~~~~~~~~~~~~~~~~~~~~~

To support the documentation built you need the following packages:

- sphinx >= 1.2.3
- sectiondoc https://github.com/enthought/sectiondoc
- mock

Alternative running :command:`pip install -r doc_requirements.txt`
should install the minimum necessary components for the documentation
built.

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

After installation the user should be able to import the ``paraview``
visualization plugin module by::

  from simphony.visualization import paraview_tools
  paraview_tools.show(cuds)

FAQ
---

- Paraview contains a separate python runtime called
  :command:`pvpython`. which python should we use?

  simphony-paraview is tested and developed using the system python on
  Ubuntu 12.04. In theory one could install simphony and
  simphony-paraview on any other python 2.7.x runtime like `pvpython`, but you
  will need to build all dependencies against the pvpython runtime environment.

- When using paraviewopenfoam and the system simphony-paraview does not work, whats wrong?

  Openfoam paraview does not make the provided python packages
  available to the system python thus in order to use the
  simphony-paraview plugin from the system python one needs to change
  the following environment variables::

    export PYTHONPATH=${PYTHONPATH}:/opt/paraviewopenfoam410/lib/paraview-4.1/site-packages/:/opt/paraviewopenfoam410/lib/paraview-4.1/site-packages/vtk
    export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/paraviewopenfoam410/lib/paraview-4.1

Known Issues
------------

- Intermittent segfault when running the test-suite (#22)
- Pressing :kbd:`a` while interacting with a view causes a segfault (#23)
- An Empty window appears when using the snapshot function (#24)

Directory structure
-------------------

- simphony-paraview -- Main package code.

  - core -- Utilities and basic conversion tools.
  
- examples -- Holds examples of visualizing simphony objects with simphony-paraview.
- doc -- Documentation related files:

  - source -- Sphinx rst source files
  - build -- Documentation build directory, if documentation has been generated
    using the ``make`` script in the ``doc`` directory.
