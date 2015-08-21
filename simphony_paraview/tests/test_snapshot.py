import os
import unittest
import tempfile
import shutil

import numpy
from PIL import Image
from hypothesis import given
from paraview import servermanager
from paraview.simple import Disconnect
from simphony.core.cuba import CUBA

from simphony_paraview.snapshot import snapshot
from simphony_paraview.core.testing import (
    cuds_containers,
    create_example_mesh, create_example_lattice, create_example_particles)


class TestSnapShot(unittest.TestCase):

    def setUp(self):
        if servermanager.ActiveConnection is not None:
            Disconnect()
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.png')
        self.addCleanup(self.cleanup)

    def tearDown(self):
        if servermanager.ActiveConnection is not None:
            raise RuntimeError('There is still an active connection')

    def cleanup(self):
        shutil.rmtree(self.temp_dir)

    @given(cuds_containers)
    def test_cuds_snapshot(self, setup):
        cuds, _ = setup
        filename = self.filename
        snapshot(cuds, filename)
        self.assertImageSavedWithContent(filename)

    def test_lattice_showing_point_data(self):
        filename = self.filename
        cuds = create_example_lattice()

        def close(obj, event):
            obj.TerminateApp()

        snapshot(cuds, filename, select=(CUBA.TEMPERATURE, 'nodes'))
        self.assertImageSavedWithContent(filename)

        with self.assertRaises(ValueError):
            snapshot(cuds, filename, select=(CUBA.TEMPERATURE, 'particles'))

        with self.assertRaises(ValueError):
            snapshot(cuds, filename, select=(CUBA.TEMPERATURE, 'points'))

    def test_particles_showing_point_data(self):
        filename = self.filename
        cuds = create_example_particles()

        snapshot(cuds, filename, select=(CUBA.TEMPERATURE, 'particles'))
        self.assertImageSavedWithContent(filename)

        with self.assertRaises(ValueError):
            snapshot(cuds, filename, select=(CUBA.TEMPERATURE, 'nodes'))

        with self.assertRaises(ValueError):
            snapshot(cuds, filename, select=(CUBA.TEMPERATURE, 'points'))

    def test_mesh_showing_cell_data(self):
        filename = self.filename
        cuds = create_example_mesh()

        snapshot(cuds, filename, select=(CUBA.TEMPERATURE, 'elements'))
        self.assertImageSavedWithContent(filename)

        with self.assertRaises(ValueError):
            snapshot(cuds, filename, select=(CUBA.TEMPERATURE, 'bonds'))

    def test_particles_showing_cell_data(self):
        filename = self.filename
        cuds = create_example_particles()

        snapshot(cuds, filename, select=(CUBA.TEMPERATURE, 'bonds'))
        self.assertImageSavedWithContent(filename)

        with self.assertRaises(ValueError):
            snapshot(cuds, filename, select=(CUBA.TEMPERATURE, 'elements'))

    def test_unknown_container(self):
        container = object()
        with self.assertRaises(TypeError):
            snapshot(container, self.filename)

    def assertImageSavedWithContent(self, filename):
        """ Load the image and check that there is some content in it.

        """
        image = numpy.asarray(Image.open(filename))

        self.assertEqual(image.shape[:2], (600, 800))
        if image.shape[2] == 3:
            check = numpy.sum(image == [0, 0, 0], axis=2) == 3
        elif image.shape[2] == 4:
            check = numpy.sum(image == [0, 0, 0, 255], axis=2) == 4
        else:
            self.fail(
                'Pixel size is not 3 or 4, but {0}'.format(image.shape[2]))
        if check.any() and check.sum() > (0.01 * 600 * 800):
            self.fail(
                'The image has to many blank spots, something is wrong')
