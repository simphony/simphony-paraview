from paraview import vtk


def iter_cells(cell_array):
    """ Iterate over the cells in a vtkCellArray. """
    cell_array.InitTraversal()
    ids = vtk.vtkIdList()
    while cell_array.GetNextCell(ids) == 1:
        yield [ids.GetId(i) for i in range(ids.GetNumberOfIds())]
