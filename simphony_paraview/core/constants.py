from collections import defaultdict

from paraview import vtk


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
