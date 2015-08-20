import unittest

from paraview.simple import (
    PointSource, Connect, Disconnect, Delete, ProgrammableFilter)
from paraview.servermanager import CreateRenderView
from simphony.core.cuba import CUBA
from hypothesis import given
from hypothesis.strategies import sampled_from

from simphony_paraview.core.paraview_utils import set_data
from simphony_paraview.core.fixes import CreateRepresentation
from simphony_paraview.core.testing import (
    add_point_data_filter_script, add_cell_data_filter_script)


class TestTypicalDistance(unittest.TestCase):

    def setUp(self):
        Connect()
        self.sources = []

    def tearDown(self):
        for source in reversed(self.sources):
            Delete(source)
        del self.sources
        Disconnect()

    @given(sampled_from(['points', 'particles', 'nodes']))
    def test_set_data_on_points(self, setup):
        # given
        view = CreateRenderView()
        source = PointSource(
            Center=(0.0, 0.0, 0.0),
            NumberOfPoints=1,
            Radius=2.0)
        self.sources.append(source)
        vtkfilter = ProgrammableFilter(
            Input=source,
            Script=add_point_data_filter_script.format(CUBA.MASS.name))
        self.sources.append(vtkfilter)

        representation = CreateRepresentation(vtkfilter, view)

        # when
        set_data(representation, vtkfilter, select=(CUBA.MASS, setup))

        # then
        self.assertEqual(representation.ColorAttributeType, 'POINT_DATA')

    @given(sampled_from(['bonds', 'elements']))
    def test_set_data_on_cells(self, setup):
        # given
        view = CreateRenderView()
        self.source = source = PointSource(
            Center=(0.0, 0.0, 0.0),
            NumberOfPoints=1,
            Radius=2.0)
        self.sources.append(source)
        vtkfilter = ProgrammableFilter(
            Input=source,
            Script=add_cell_data_filter_script.format(CUBA.MASS.name))
        self.sources.append(vtkfilter)

        representation = CreateRepresentation(vtkfilter, view)

        # when
        set_data(representation, vtkfilter, select=(CUBA.MASS, setup))

        # then
        self.assertEqual(representation.ColorAttributeType, 'CELL_DATA')

    def test_set_data_on_invalid(self):
        # given
        view = CreateRenderView()
        self.source = source = PointSource(
            Center=(0.0, 0.0, 0.0),
            NumberOfPoints=1,
            Radius=2.0)
        self.sources.append(source)
        vtkfilter = ProgrammableFilter(
            Input=source,
            Script=add_cell_data_filter_script.format(CUBA.MASS.name))
        self.sources.append(vtkfilter)
        representation = CreateRepresentation(vtkfilter, view)

        # when/then
        with self.assertRaises(ValueError):
            set_data(representation, vtkfilter, select=(CUBA.MASS, 'cells'))
