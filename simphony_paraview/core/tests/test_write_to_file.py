import unittest
import tempfile
import shutil
import os

from hypothesis import given
from paraview.simple import OpenDataFile, Delete, Connect, Disconnect
from paraview import servermanager

from simphony_paraview.core.api import write_to_file
from simphony_paraview.core.testing import cuds_containers


class TestWriteToFile(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.vtk')
        self.addCleanup(self.cleanup)
        if servermanager.ActiveConnection is not None:
            Disconnect()

    def tearDown(self):
        if servermanager.ActiveConnection is not None:
            raise RuntimeError('There is still an active connection')

    def cleanup(self):
        shutil.rmtree(self.temp_dir)

    @given(cuds_containers)
    def test_write(self, setup):
        # given
        cuds, kind = setup
        filename = self.filename

        # when
        write_to_file(cuds, filename)

        # then
        self.assertTrue(os.path.exists(self.filename))
        Connect()
        reader = None
        try:
            reader = OpenDataFile(filename)
            info = reader.GetDataInformation()
            self.assertEqual(info.GetDataSetType(), kind)
        except Exception as exc:
            print exc
            raise
        finally:
            if reader is not None:
                Delete(reader)
            Disconnect()
