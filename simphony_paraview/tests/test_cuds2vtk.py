import unittest
import itertools
from functools import partial

import numpy
from numpy.testing import assert_array_equal
from hypothesis import given
from hypothesis.strategies import sampled_from
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from simphony.cuds import (
    Particle, Bond, Particles, LatticeNode, Mesh, Point)
from simphony.cuds.lattice import (
    make_hexagonal_lattice, make_cubic_lattice, make_square_lattice,
    make_rectangular_lattice, make_orthorombicp_lattice)
from simphony.testing.utils import (
    compare_data_containers, compare_particles, compare_bonds, compare_points)

from simphony_paraview.cuds2vtk import cuds2vtk

lattice_types = sampled_from([
    make_square_lattice('test', 0.1, (3, 6)),
    make_cubic_lattice('test', 0.1, (3, 6, 5)),
    make_hexagonal_lattice('test', 0.1, (5, 4)),
    make_rectangular_lattice('test', (0.1, 0.3), (3, 6)),
    make_orthorombicp_lattice('test', (0.1, 0.2, 0.1), (3, 7, 6))])


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

    def _test_with_cuds_particles(self):
        # given
        points = [
            [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        bonds = [[0, 1], [0, 3], [1, 3, 2]]
        point_temperature = [10., 20., 30., 40.]
        bond_temperature = [60., 80., 190., 5.]

        cuds = Particles('test')
        particle_uids = cuds.add_particles(
            Particle(
                coordinates=point,
                data=DataContainer(TEMPERATURE=point_temperature[index]))
            for index, point in enumerate(points))
        bond_uids = cuds.add_bonds(
            Bond(
                particles=[particle_uids[index] for index in indices],
                data=DataContainer(TEMPERATURE=bond_temperature[index]))
            for index, indices in enumerate(bonds))

        # when
        data_set = cuds2vtk(cuds)

        # then
        self.assertEqual(data_set.NumberOfPoints, len(particle_uids))
        for expected in reference.iter_particles():
            self.assertEqual(container.get_particle(expected.uid), expected)
        number_of_bonds = sum(1 for _ in container.iter_bonds())
        self.assertEqual(number_of_bonds, len(bond_uids))
        for expected in reference.iter_bonds():
            self.assertEqual(container.get_bond(expected.uid), expected)

    @given(lattice_types)
    def _test_cuds_lattice(self, lattice):
        # when
        vtk_lattice = VTKLattice.from_lattice(lattice)

        # then
        xspace, yspace, _ = lattice.base_vect
        self.assertEqual(vtk_lattice.type, lattice.type)
        self.assertEqual(vtk_lattice.data, lattice.data)
        self.assertEqual(vtk_lattice.size, lattice.size)
        assert_array_equal(vtk_lattice.origin, lattice.origin)
        assert_array_equal(vtk_lattice.base_vect, lattice.base_vect)

    def _test_with_cuds_mesh(self):
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
            for index, point in enumerate(self.points)]

        container = Mesh('test')
        for point in points:
            container.add_point(point)

        faces = [
            Face(
                points=[points[index].uid for index in face],
                data=DataContainer(TEMPERATURE=next(count)))
            for face in self.faces]
        edges = [
            Edge(
                points=[points[index].uid for index in edge],
                data=DataContainer(TEMPERATURE=next(count)))
            for edge in self.edges]
        cells = [
            Cell(
                points=[points[index].uid for index in cell],
                data=DataContainer(TEMPERATURE=next(count)))
            for cell in self.cells]
        for edge in edges:
            container.add_edge(edge)
        for face in faces:
            container.add_face(face)
        for cell in cells:
            container.add_cell(cell)

        # when
        vtk_container = VTKMesh.from_mesh(container)

        # then
        self.assertEqual(vtk_container.name, container.name)
        self.assertEqual(sum(1 for _ in vtk_container.iter_points()), 12)
        self.assertEqual(sum(1 for _ in vtk_container.iter_edges()), 2)
        self.assertEqual(sum(1 for _ in vtk_container.iter_faces()), 1)
        self.assertEqual(sum(1 for _ in vtk_container.iter_cells()), 2)
        for point in points:
            self.assertEqual(vtk_container.get_point(point.uid), point)
        for edge in edges:
            self.assertEqual(vtk_container.get_edge(edge.uid), edge)
        for face in faces:
            self.assertEqual(vtk_container.get_face(face.uid), face)
        for cell in cells:
            self.assertEqual(vtk_container.get_cell(cell.uid), cell)

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

if __name__ == '__main__':
    unittest.main()
