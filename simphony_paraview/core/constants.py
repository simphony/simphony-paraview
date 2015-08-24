import enum
from collections import defaultdict

import numpy
from paraview import vtk
from paraview import vtkConstants
from paraview.vtk import io

from .cuba_utils import supported_cuba, default_cuba_value


class VALUETYPES(enum.IntEnum):

    SCALAR = 0
    VECTOR = 1
    STRING = 2


def points2edge():
    """ Return a mapping from number of points to line cells. """
    return defaultdict(
        lambda: vtk.vtkPolyLine().GetCellType(),
        {2: vtk.vtkLine().GetCellType()})


def points2face():
    """ Return a mapping from number of points to face cells. """
    return defaultdict(
        lambda: vtk.Polygon().GetCellType(),
        {3: vtk.vtkTriangle().GetCellType(), 4: vtk.vtkQuad().GetCellType()})


def points2cell():
    """ Return a mapping from number of points to volume cells. """
    return {
        4: vtk.vtkTetra().GetCellType(),
        8: vtk.vtkHexahedron().GetCellType(),
        6: vtk.vtkWedge().GetCellType(),
        5: vtk.vtkPyramid().GetCellType(),
        10: vtk.vtkPentagonalPrism().GetCellType(),
        12: vtk.vtkHexagonalPrism().GetCellType()}


def dataset2writer():
    """ Return a mapping from dataset type to writer instances. """
    return {
        vtkConstants.VTK_UNSTRUCTURED_GRID: io.vtkUnstructuredGridWriter,
        vtkConstants.VTK_STRUCTURED_POINTS: io.vtkStructuredPointsWriter,
        vtkConstants.VTK_POLY_DATA: io.vtkPolyDataWriter}


def cuba_value_types():
    """ Return a mapping from CUBA to VALUETYPE. """
    types = {}
    for cuba in supported_cuba():
        default = default_cuba_value(cuba)
        if isinstance(default, (float, int, long)):
            types[cuba] = VALUETYPES.SCALAR
        elif isinstance(default, str):
            types[cuba] = VALUETYPES.STRING
        elif isinstance(default, numpy.ndarray):
            types[cuba] = VALUETYPES.VECTOR
    return types
