import unittest

from hypothesis import given
from paraview import servermanager
from paraview.simple import Disconnect
from simphony.core.cuba import CUBA

from simphony_paraview.show import show
from simphony_paraview.core.testing import (
    cuds_containers,
    create_example_mesh, create_example_lattice, create_example_particles)


class TestShow(unittest.TestCase):

    def setUp(self):
        if servermanager.ActiveConnection is not None:
            Disconnect()
        self.closed = False

    def tearDown(self):
        if servermanager.ActiveConnection is not None:
            raise RuntimeError('There is still an active connection')

    @given(cuds_containers)
    def test_valid_cuds_containers(self, setup):
        # XXX This is a very basic test.
        # given
        cuds, kind = setup

        def close(obj, event):
            obj.TerminateApp()

        show(cuds, testing=close)

    def test_lattice_showing_point_data(self):
        cuds = create_example_lattice()

        def close(obj, event):
            obj.TerminateApp()

        show(cuds, select=(CUBA.TEMPERATURE, 'nodes'), testing=close)

        with self.assertRaises(ValueError):
            show(cuds, select=(CUBA.TEMPERATURE, 'particles'), testing=close)

        with self.assertRaises(ValueError):
            show(cuds, select=(CUBA.TEMPERATURE, 'points'), testing=close)

    def test_mesh_showing_point_data(self):
        cuds = create_example_mesh()

        def close(obj, event):
            obj.TerminateApp()

        show(cuds, select=(CUBA.TEMPERATURE, 'points'), testing=close)

        with self.assertRaises(ValueError):
            show(cuds, select=(CUBA.TEMPERATURE, 'nodes'), testing=close)

        with self.assertRaises(ValueError):
            show(cuds, select=(CUBA.TEMPERATURE, 'partiles'), testing=close)

    def test_particles_showing_point_data(self):
        cuds = create_example_particles()

        def close(obj, event):
            obj.TerminateApp()

        show(cuds, select=(CUBA.TEMPERATURE, 'particles'), testing=close)

        with self.assertRaises(ValueError):
            show(cuds, select=(CUBA.TEMPERATURE, 'nodes'), testing=close)

        with self.assertRaises(ValueError):
            show(cuds, select=(CUBA.TEMPERATURE, 'points'), testing=close)

    def test_mesh_showing_cell_data(self):
        cuds = create_example_mesh()

        def close(obj, event):
            obj.TerminateApp()

        show(cuds, select=(CUBA.TEMPERATURE, 'elements'), testing=close)

        with self.assertRaises(ValueError):
            show(cuds, select=(CUBA.TEMPERATURE, 'bonds'), testing=close)

    def test_particles_showing_cell_data(self):
        cuds = create_example_particles()

        def close(obj, event):
            obj.TerminateApp()

            show(cuds, select=(CUBA.TEMPERATURE, 'bonds'), testing=close)

        with self.assertRaises(ValueError):
            show(cuds, select=(CUBA.TEMPERATURE, 'elements'), testing=close)

    def test_unknown_container(self):
        container = object()
        with self.assertRaises(TypeError):
            show(container)
