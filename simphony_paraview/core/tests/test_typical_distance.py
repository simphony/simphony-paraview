import unittest

from paraview.simple import PointSource, Connect, Disconnect, Delete, Line

from simphony_paraview.core.paraview_utils import typical_distance


class TestTypicalDistance(unittest.TestCase):

    def setUp(self):
        Connect()

    def tearDown(self):
        Disconnect()

    def test_single_point(self):
        # given
        source = PointSource(
            Center=(0.0, 0.0, 0.0),
            NumberOfPoints=1,
            Radius=2.0)

        try:
            # when
            distance = typical_distance(source)
        finally:
            Delete(source)

        # then
        self.assertEqual(distance, 1.0)

    def test_basic_usage(self):
        # given
        source = Line()
        try:
            # when
            distance = typical_distance(source)
        finally:
            Delete(source)

        # then
        info = source.GetDataInformation()
        expected = 0.5 / info.GetNumberOfPoints()
        self.assertAlmostEqual(distance, expected)
