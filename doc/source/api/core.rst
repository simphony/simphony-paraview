Core module
===========

A module containing core tools and wrappers for paraview data containers
used in simphony_paraview.

.. rubric:: Classes

.. currentmodule:: simphony_paraview.core

.. autosummary::

    ~cuba_data_accumulator.CUBADataAccumulator

.. rubric:: Functions

.. autosummary::

   ~cuba_utils.supported_cuba
   ~cuba_utils.default_cuba_value
   ~cuds2vtk.cuds2vtk

.. rubric:: Mappings

.. autosummary::

   ~constants.points2edge
   ~constants.points2face
   ~constants.points2cell
   ~constants.dataset2writer
   ~constants.cuba_value_types


Description
-----------

.. autoclass:: simphony_paraview.core.cuba_data_accumulator.CUBADataAccumulator
     :members:
     :special-members: __getitem__, __len__
     :undoc-members:
     :show-inheritance:

----------------------------

.. autofunction:: simphony_paraview.core.cuba_utils.supported_cuba

.. autofunction:: simphony_paraview.core.cuba_utils.default_cuba_value

.. autofunction:: simphony_paraview.core.cuds2vtk.cuds2vtk

-----------------------------

.. autofunction:: simphony_paraview.core.constants.points2edge

.. autofunction:: simphony_paraview.core.constants.points2face

.. autofunction:: simphony_paraview.core.constants.points2cell

.. autofunction:: simphony_paraview.core.constants.dataset2writer

.. autofunction:: simphony_paraview.core.constants.cuba_value_types
