import unittest
import itertools
from functools import partial

import numpy
from numpy.testing import assert_array_equal
from paraview.numpy_support import vtk_to_numpy
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from simphony.cuds import (
    Particle, Bond, Particles, Mesh, Point, Edge, Cell, Face)
from simphony.cuds.lattice import (
    make_hexagonal_lattice, make_cubic_lattice, make_square_lattice,
    make_rectangular_lattice, make_orthorombicp_lattice)
from simphony.testing.utils import (
    compare_data_containers, compare_particles, compare_bonds, compare_points)

from simphony_paraview.cuds2vtk import cuds2vtk
from simphony_paraview.core.api import (
    iter_cells, iter_grid_cells, points2edge, points2face, points2cell)


class TestCUDS2VTK(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(
            DataContainer, partial(compare_data_containers, testcase=self))
        self.addTypeEqualityFunc(
            Point, partial(compare_points, testcase=self))
        self.addTypeEqualityFunc(
            Particle, partial(compare_particles, testcase=self))
        self.addTypeEqualityFunc(
            Bond, partial(compare_bonds, testcase=self))

    def test_with_cuds_particles(self):
        # given
        points = [
            [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        bonds = [[0, 1], [0, 3], [1, 3, 2]]
        point_temperature = [10., 20., 30., 40.]
        bond_temperature = [60., 80., 190.]

        cuds = Particles('test')
        particle_uids = cuds.add_particles(
            Particle(
                coordinates=point,
                data=DataContainer(
                    TEMPERATURE=point_temperature[index],
                    MASS=index))
            for index, point in enumerate(points))
        cuds.add_bonds(
            Bond(
                particles=[particle_uids[uid] for uid in indices],
                data=DataContainer(
                    TEMPERATURE=bond_temperature[index],
                    MASS=index))
            for index, indices in enumerate(bonds))

        # when
        data_set = cuds2vtk(cuds)

        # then check points
        self.assertEqual(data_set.GetNumberOfPoints(), 4)

        coordinates = [
            particle.coordinates for particle in cuds.iter_particles()]
        vtk_points = [
            data_set.GetPoint(index)
            for index in range(len(particle_uids))]
        self.assertItemsEqual(vtk_points, coordinates)

        point_data = data_set.GetPointData()
        self.assertEqual(point_data.GetNumberOfArrays(), 2)
        arrays = {
            point_data.GetArray(index).GetName(): point_data.GetArray(index)
            for index in range(2)}
        self.assertItemsEqual(arrays.keys(), ['MASS', 'TEMPERATURE'])
        mass = vtk_to_numpy(arrays['MASS'])
        self.assertItemsEqual(mass, range(4))
        assert_array_equal(
            vtk_to_numpy(arrays['TEMPERATURE']),
            [point_temperature[int(index)] for index in mass])

        # then check bonds
        self.assertEqual(data_set.GetNumberOfCells(), 3)

        links = [[
            particle.coordinates
            for particle in cuds.iter_particles(bond.particles)]
            for bond in cuds.iter_bonds()]
        vtk_lines = data_set.GetLines()
        lines = [[
            data_set.GetPoint(index) for index in line]
            for line in iter_cells(vtk_lines)]
        self.assertItemsEqual(lines, links)

        cell_data = data_set.GetCellData()
        self.assertEqual(cell_data.GetNumberOfArrays(), 2)
        arrays = {
            cell_data.GetArray(index).GetName(): cell_data.GetArray(index)
            for index in range(2)}
        self.assertItemsEqual(arrays.keys(), ['MASS', 'TEMPERATURE'])
        mass = vtk_to_numpy(arrays['MASS'])
        self.assertItemsEqual(mass, range(3))
        assert_array_equal(
            vtk_to_numpy(arrays['TEMPERATURE']),
            [bond_temperature[int(index)] for index in mass])

    def test_source_from_a_xy_plane_square_lattice(self):
        # given
        shape = 2, 4
        lattice = make_square_lattice(
            'test', 0.2, (2, 4), origin=(0.2, -2.4, 0.0))
        self.add_velocity(lattice)

        # when
        data_set = cuds2vtk(cuds=lattice)

        # then
        self.assertEqual(data_set.GetNumberOfPoints(), numpy.prod(shape))
        assert_array_equal(data_set.GetOrigin(), (0.2, -2.4, 0.0))

        point_data = data_set.GetPointData()
        arrays = {
            point_data.GetArray(index).GetName():
            vtk_to_numpy(point_data.GetArray(index))
            for index in range(point_data.GetNumberOfArrays())}
        for node in lattice.iter_nodes():
            point_id = data_set.ComputePointId(node.index)
            assert_array_equal(
                lattice.get_coordinate(node.index),
                data_set.GetPoint(point_id))
            for key, value in node.data.iteritems():
                assert_array_equal(arrays[key.name][point_id], value)

    def test_source_from_a_xy_plane_rectangular_lattice(self):
        # given
        lattice = make_rectangular_lattice(
            'test', (0.3, 0.35), (13, 23), origin=(0.2, -2.7, 0.0))
        self.add_velocity(lattice)

        # when
        data_set = cuds2vtk(cuds=lattice)

        # then
        self.assertEqual(data_set.GetNumberOfPoints(), 13 * 23)
        assert_array_equal(data_set.GetOrigin(), (0.2, -2.7, 0.0))

        point_data = data_set.GetPointData()
        arrays = {
            point_data.GetArray(index).GetName():
            vtk_to_numpy(point_data.GetArray(index))
            for index in range(point_data.GetNumberOfArrays())}
        for node in lattice.iter_nodes():
            point_id = data_set.ComputePointId(node.index)
            assert_array_equal(
                lattice.get_coordinate(node.index),
                data_set.GetPoint(point_id))
            for key, value in node.data.iteritems():
                assert_array_equal(arrays[key.name][point_id], value)

    def test_source_from_a_cubic_lattice(self):
        # given
        lattice = make_cubic_lattice('test', 0.4, (14, 24, 34), (4, 5, 6))
        self.add_velocity(lattice)

        # when
        data_set = cuds2vtk(cuds=lattice)

        # then
        self.assertEqual(data_set.GetNumberOfPoints(), 14 * 24 * 34)
        assert_array_equal(data_set.GetOrigin(), (4.0, 5.0, 6.0))

        point_data = data_set.GetPointData()
        arrays = {
            point_data.GetArray(index).GetName():
            vtk_to_numpy(point_data.GetArray(index))
            for index in range(point_data.GetNumberOfArrays())}
        for node in lattice.iter_nodes():
            point_id = data_set.ComputePointId(node.index)
            assert_array_equal(
                lattice.get_coordinate(node.index),
                data_set.GetPoint(point_id))
            for key, value in node.data.iteritems():
                assert_array_equal(arrays[key.name][point_id], value)

    def test_source_from_an_orthorombic_p_lattice(self):
        # given
        lattice = make_orthorombicp_lattice(
            'test',  (0.5, 0.54, 0.58), (15, 25, 35), (7, 9, 8))
        self.add_velocity(lattice)

        # when
        data_set = cuds2vtk(cuds=lattice)

        # then
        self.assertEqual(data_set.GetNumberOfPoints(), 15 * 25 * 35)
        assert_array_equal(data_set.GetOrigin(), (7.0, 9.0, 8.0))

        point_data = data_set.GetPointData()
        arrays = {
            point_data.GetArray(index).GetName():
            vtk_to_numpy(point_data.GetArray(index))
            for index in range(point_data.GetNumberOfArrays())}
        for node in lattice.iter_nodes():
            point_id = data_set.ComputePointId(node.index)
            assert_array_equal(
                lattice.get_coordinate(node.index),
                data_set.GetPoint(point_id))
            for key, value in node.data.iteritems():
                assert_array_equal(arrays[key.name][point_id], value)

    def test_source_from_a_xy_plane_hexagonal_lattice(self):
        # given
        lattice = make_hexagonal_lattice('test', 0.1, (5, 4))
        self.add_velocity(lattice)

        # when
        data_set = cuds2vtk(cuds=lattice)

        # then
        self.assertEqual(data_set.GetNumberOfPoints(), 5 * 4)
        xspace, yspace, _ = lattice.base_vect

        points = vtk_to_numpy(data_set.GetPoints().GetData())
        for node in lattice.iter_nodes():
            position = lattice.get_coordinate(node.index)
            point_id = data_set.FindPoint(position)
            assert_array_equal(
                points[point_id], numpy.asarray(position, dtype=points.dtype))

    def test_with_cuds_mesh(self):
        # given
        points = numpy.array([
            [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
            [2, 0, 0], [3, 0, 0], [3, 1, 0], [2, 1, 0],
            [2, 0, 1], [3, 0, 1], [3, 1, 1], [2, 1, 1]],
            'f')
        cells = [
            [0, 1, 2, 3],  # tetra
            [4, 5, 6, 7, 8, 9, 10, 11]]  # hex
        faces = [[2, 7, 11]]
        edges = [[1, 4], [3, 8]]
        count = itertools.count()
        points = [
            Point(coordinates=point, data=DataContainer(TEMPERATURE=index))
            for index, point in enumerate(points)]

        cuds = Mesh('test')
        cuds.add_points(points)

        faces = [
            Face(
                points=[points[index].uid for index in face],
                data=DataContainer(TEMPERATURE=next(count)))
            for face in faces]
        edges = [
            Edge(
                points=[points[index].uid for index in edge],
                data=DataContainer(TEMPERATURE=next(count)))
            for edge in edges]
        cells = [
            Cell(
                points=[points[index].uid for index in cell],
                data=DataContainer(TEMPERATURE=next(count)))
            for cell in cells]
        cuds.add_edges(edges)
        cuds.add_faces(faces)
        cuds.add_cells(cells)

        # when
        data_set = cuds2vtk(cuds=cuds)

        # then check points
        self.assertEqual(data_set.GetNumberOfPoints(), 12)

        point_data = data_set.GetPointData()
        self.assertEqual(point_data.GetNumberOfArrays(), 1)
        temperature = point_data.GetArray(0)
        self.assertEqual(temperature.GetName(), 'TEMPERATURE')
        self.assertItemsEqual(
            vtk_to_numpy(temperature), range(12))

        # then check cells
        self.assertEqual(data_set.GetNumberOfCells(), 5)

        cell_data = data_set.GetCellData()
        self.assertEqual(cell_data.GetNumberOfArrays(), 1)
        temperature = cell_data.GetArray(0)
        self.assertEqual(temperature.GetName(), 'TEMPERATURE')
        self.assertItemsEqual(
            vtk_to_numpy(temperature), range(5))

        # For each cell in the container
        # find the corresponding cell in the vtkCellArray and
        # verify that they link to points that have the right coordinates.
        for cell in itertools.chain(
                cuds.iter_edges(), cuds.iter_faces(), cuds.iter_cells()):
            # The temperature value is also the index that the cells
            # are expected to have in the vtkCellArray.
            value = cell.data[CUBA.TEMPERATURE]
            index = numpy.nonzero(vtk_to_numpy(temperature) == value)[0]
            vtk_cell = data_set.GetCell(index)
            ids = vtk_cell.GetPointIds()
            for i, uid in enumerate(cell.points):
                cell_point = cuds.get_point(uid)
                assert_array_equal(
                    data_set.GetPoint(ids.GetId(i)), cell_point.coordinates)

    def test_with_empty_cuds_mesh(self):
        # given
        cuds = Mesh('test')

        # when
        data_set = cuds2vtk(cuds)

        # then
        self.assertEqual(data_set.GetNumberOfPoints(), 0)
        self.assertEqual(data_set.GetNumberOfCells(), 0)

    def test_with_empty_cuds_particles(self):
        # given
        cuds = Particles('test')

        # when
        data_set = cuds2vtk(cuds)

        # then
        self.assertEqual(data_set.GetNumberOfPoints(), 0)
        self.assertEqual(data_set.GetNumberOfCells(), 0)

    def add_velocity(self, lattice):
        nodes = [node for node in lattice.iter_nodes()]
        for node in nodes:
            node.data[CUBA.VELOCITY] = node.index
        lattice.update_nodes(nodes)


if __name__ == '__main__':
    unittest.main()
