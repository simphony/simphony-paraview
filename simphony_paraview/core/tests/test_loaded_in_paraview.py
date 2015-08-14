import unittest

from hypothesis import given
from paraview import servermanager
from paraview.simple import Connect, Disconnect, GetActiveSource

from simphony_paraview.core.api import loaded_in_paraview
from simphony_paraview.core.testing import cuds_containers


class TestLoadedInParaview(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        if servermanager.ActiveConnection is not None:
            raise RuntimeError('There is still an active connection')

    @given(cuds_containers)
    def test_loadded_with_no_active_connection(self, setup):
        # given
        cuds, kind = setup

        # when/then
        with loaded_in_paraview(cuds) as source:
            info = source.GetDataInformation()
            self.assertEqual(info.GetDataSetType(), kind)

    @given(cuds_containers)
    def test_loadded_with_active_connection(self, setup):
        # given
        cuds, kind = setup

        # when/then
        connection = Connect()
        try:
            with loaded_in_paraview(cuds) as source:
                info = source.GetDataInformation()
                self.assertEqual(info.GetDataSetType(), kind)
                self.assertEqual(servermanager.ActiveConnection, connection)
                self.assertEqual(GetActiveSource(), source)
            self.assertEqual(GetActiveSource(), None)
        finally:
            if servermanager.ActiveConnection is connection:
                Disconnect()
