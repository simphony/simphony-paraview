from paraview import vtk
from paraview.numpy_support import vtk_to_numpy


def iter_cells(cell_array):
    """ Iterate over the cells in a vtkCellArray. """
    cell_array.InitTraversal()
    ids = vtk.vtkIdList()
    while cell_array.GetNextCell(ids) == 1:
        yield [ids.GetId(i) for i in range(ids.GetNumberOfIds())]


def iter_grid_cells(grid, cell_types=None):
    """ Iterate over cells in a vtkUnstructuredGrid filtering on CellTypes. """
    if cell_types is None:
        for index in range(grid.GetNumberOfCells()):
            cell = grid.GetCell(index)
            ids = cell.GetPointIds()
            yield [ids.GetId(i) for i in range(ids.GetNumberOfIds())]
    else:
        cell_types_array = vtk_to_numpy(grid.GetCellTypesArray())
        for index, cell_type in enumerate(cell_types_array):
            if cell_type in cell_types:
                cell = grid.GetCell(index)
                ids = cell.GetPointIds()
                yield [ids.GetId(i) for i in range(ids.GetNumberOfIds())]
