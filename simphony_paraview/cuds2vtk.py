from paraview import vtk
from simphony.cuds import ABCMesh, ABCParticles, ABCLattice

from simphony_paraview.core.api import CUBADataAccumulator


def cuds2vtk(cuds):
    """ Create a vtk.Dataset from a CUDS container """

    if isinstance(cuds, ABCMesh):
        data_set = vtk.vtkUnstructuredGrid()
    elif isinstance(cuds, ABCParticles):
        data_set = _particles2polydata(cuds)
    elif isinstance(cuds, ABCLattice):
        data_set = vtk.vtkImageData()

    return data_set


def _particles2polydata(cuds):
    particle2index = {}
    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()
    polydata = vtk.vtkPolyData()
    point_data = polydata.GetPointData()
    cell_data = polydata.GetCellData()
    data_collector = CUBADataAccumulator(container=point_data)
    for index, particle in enumerate(cuds.iter_particles()):
        particle2index[particle.uid] = index
        points.InsertPoint(index, *particle.coordinates)
        data_collector.append(particle.data)
    data_collector = CUBADataAccumulator(container=cell_data)
    for bond in cuds.iter_bonds():
        lines.InsertNextCell(len(bond.particles))
        for uuid in bond.particles:
            lines.InsertCellPoint(particle2index[uuid])
        data_collector.append(bond.data)
    polydata.SetPoints(points)
    polydata.SetLines(lines)
    return polydata
