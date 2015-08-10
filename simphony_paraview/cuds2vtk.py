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
        lattice_type = cuds.type
        if lattice_type in (
                'Cubic', 'OrthorombicP', 'Square', 'Rectangular'):
            data_set = _lattice2StructuredPoints(cuds)
        elif lattice_type == 'Hexagonal':
            data_set = _lattice2PolyData(cuds)

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
def _lattice2StructuredPoints(cuds):
    origin = cuds.origin
    size = cuds.size
    spacing = cuds.base_vect

    structured_points = vtk.vtkStructuredPoints()
    structured_points.SetSpacing(spacing)
    structured_points.SetOrigin(origin)
    structured_points.SetExtent(0, size[0] - 1, 0, size[1] - 1, 0, size[2] - 1)

    y, z, x = numpy.meshgrid(
        range(size[1]), range(size[2]), range(size[0]))
    indices = izip(x.ravel(), y.ravel(), z.ravel())
    point_data = structured_points.GetPointData()
    data_collector = CUBADataAccumulator(container=point_data)
    for node in cuds.iter_nodes(indices):
        data_collector.append(node.data)

    return structured_points


def _lattice2PolyData(cuds):
    polydata = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    coordinates = cuds.get_coordinate

    point_data = polydata.GetPointData()
    data_collector = CUBADataAccumulator(container=point_data)
    for node in cuds.iter_nodes():
        points.InsertNextPoint(coordinates(node.index))
        data_collector.append(node.data)

    polydata.SetPoints(points)
    return polydata
