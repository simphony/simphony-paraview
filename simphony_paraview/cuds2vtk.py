from itertools import izip

import numpy
from paraview import vtk
from simphony.cuds import ABCMesh, ABCParticles, ABCLattice

from simphony_paraview.core.api import (
    CUBADataAccumulator, points2edge, points2face, points2cell)


def cuds2vtk(cuds):
    """ Create a vtk.Dataset from a CUDS container """

    if isinstance(cuds, ABCMesh):
        data_set = _mesh2unstructured_grid(cuds)
    elif isinstance(cuds, ABCParticles):
        data_set = _particles2poly_data(cuds)
    elif isinstance(cuds, ABCLattice):
        lattice_type = cuds.type
        if lattice_type in (
                'Cubic', 'OrthorombicP', 'Square', 'Rectangular'):
            data_set = _lattice2structured_points(cuds)
        elif lattice_type == 'Hexagonal':
            data_set = _lattice2poly_data(cuds)
    else:
        msg = 'Provided object {} is not of any known cuds container types'
        raise TypeError(msg.format(type(cuds)))

    return data_set


def _particles2poly_data(cuds):
    particle2index = {}
    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()
    poly_data = vtk.vtkPolyData()

    point_data = poly_data.GetPointData()
    data_collector = CUBADataAccumulator(container=point_data)
    for index, particle in enumerate(cuds.iter_particles()):
        particle2index[particle.uid] = index
        points.InsertPoint(index, *particle.coordinates)
        data_collector.append(particle.data)

    cell_data = poly_data.GetCellData()
    data_collector = CUBADataAccumulator(container=cell_data)
    for bond in cuds.iter_bonds():
        lines.InsertNextCell(len(bond.particles))
        for uuid in bond.particles:
            lines.InsertCellPoint(particle2index[uuid])
        data_collector.append(bond.data)

    poly_data.SetPoints(points)
    poly_data.SetLines(lines)
    return poly_data


def _lattice2structured_points(cuds):
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


def _lattice2poly_data(cuds):
    poly_data = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    coordinates = cuds.get_coordinate

    # copy node data
    point_data = poly_data.GetPointData()
    data_collector = CUBADataAccumulator(container=point_data)
    for node in cuds.iter_nodes():
        points.InsertNextPoint(coordinates(node.index))
        data_collector.append(node.data)

    poly_data.SetPoints(points)
    return poly_data


def _mesh2unstructured_grid(cuds):
    point2index = {}
    unstructured_grid = vtk.vtkUnstructuredGrid()
    unstructured_grid.Allocate()

    # copy points
    points = vtk.vtkPoints()
    point_data = unstructured_grid.GetPointData()
    data_collector = CUBADataAccumulator(container=point_data)
    for index, point in enumerate(cuds.iter_points()):
        point2index[point.uid] = index
        points.InsertNextPoint(*point.coordinates)
        data_collector.append(point.data)

    # prepare to copy elements
    cell_data = unstructured_grid.GetCellData()
    data_collector = CUBADataAccumulator(container=cell_data)

    # copy edges
    mapping = points2edge()
    for edge in cuds.iter_edges():
        npoints = len(edge.points)
        ids = vtk.vtkIdList()
        for uid in edge.points:
            ids.InsertNextId(point2index[uid])
        unstructured_grid.InsertNextCell(mapping[npoints], ids)
        data_collector.append(edge.data)

    # copy faces
    mapping = points2face()
    for face in cuds.iter_faces():
        npoints = len(face.points)
        ids = vtk.vtkIdList()
        for uid in face.points:
            ids.InsertNextId(point2index[uid])
        unstructured_grid.InsertNextCell(mapping[npoints], ids)
        data_collector.append(face.data)

    # copy cells
    mapping = points2cell()
    for cell in cuds.iter_cells():
        npoints = len(cell.points)
        ids = vtk.vtkIdList()
        for uid in cell.points:
            ids.InsertNextId(point2index[uid])
        unstructured_grid.InsertNextCell(mapping[npoints], ids)
        data_collector.append(cell.data)

    unstructured_grid.SetPoints(points)
    return unstructured_grid