import unittest

from hypothesis import given
from paraview import servermanager
from paraview.simple import Disconnect

from simphony_paraview.show import show
from simphony_paraview.core.testing import cuds_containers


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

        show(cuds, close)

    def test_unknown_container(self):
        container = object()
        with self.assertRaises(TypeError):
            show(container)
