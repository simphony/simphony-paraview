import os
import unittest
import tempfile
import shutil

import numpy
from PIL import Image


from simphony_paraview.snapshot import snapshot
from simphony.cuds.lattice import make_square_lattice
from simphony.cuds.mesh import Mesh, Point
from simphony.cuds.particles import Particles, Particle


class TestSnapShot(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.png')
        self.addCleanup(self.cleanup)

    def cleanup(self):
        shutil.rmtree(self.temp_dir)

    def test_lattice_snapshot(self):
        filename = self.filename
        lattice = make_square_lattice(
            'test', 0.2, (10, 10), origin=(0.2, -2.4))
        snapshot(lattice, filename)
        self.assertImageSavedWithContent(filename)

    def test_mesh_snapshot(self):
        filename = self.filename
        points = numpy.array([
            [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
            [2, 0, 0], [3, 0, 0], [3, 1, 0], [2, 1, 0],
            [2, 0, 1], [3, 0, 1], [3, 1, 1], [2, 1, 1]],
            'f')
        mesh = Mesh('test')
        items = [Point(coordinates=point) for index, point in enumerate(points)]
        mesh.add_points(items)

        snapshot(mesh, filename)
        self.assertImageSavedWithContent(filename)

    def test_particles_snapshot(self):
        filename = self.filename
        coordinates = numpy.array([
            [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
            [2, 0, 0], [3, 0, 0], [3, 1, 0], [2, 1, 0],
            [2, 0, 1], [3, 0, 1], [3, 1, 1], [2, 1, 1]],
            'f')
        particles = Particles('test')
        items = [Particle(coordinates=point + 3) for index, point in enumerate(coordinates)]
        particles.add_particles(items)

        snapshot(particles, filename)
        self.assertImageSavedWithContent(filename)

    def test_snapshot_invalid_cuds(self):
        filename = self.filename
        with self.assertRaises(TypeError):
            snapshot(object(), filename)

    def assertImageSavedWithContent(self, filename):
        """ Load the image and check that there is some content in it.

        """
        image = numpy.array(Image.open(filename))

        self.assertEqual(image.shape[:2], (600, 800))
        if image.shape[2] == 3:
            check = numpy.sum(image == [0, 0, 0], axis=2) == 3
        elif image.shape[2] == 4:
            check = numpy.sum(image == [0, 0, 0, 255], axis=2) == 4
        else:
            self.fail(
                'Pixel size is not 3 or 4, but {0}'.format(image.shape[2]))
        if check.any():
            self.fail('The image has blank spots, something is wrong')
