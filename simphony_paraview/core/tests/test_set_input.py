import unittest

from hypothesis import given
from hypothesis.strategies import sampled_from
from mock import patch, Mock

from simphony_paraview.core.compatibility import set_input


class TestSetInput(unittest.TestCase):

    @given(sampled_from(('5.8.0', '6.1.0')))
    def test_set_input_with_valid_vtk(self, version):
        source = Mock()
        input = Mock()

        module_path = 'simphony_paraview.core.compatibility.VTK_VERSION'
        with patch(module_path) as VTK_VERSION:
            VTK_VERSION.__getitem__ = lambda x, y: version[y]
            set_input(source, input)

    @given(sampled_from(('3.4.0', '7.3.0')))
    def test_set_input_with_invalid_vtk(self, version):
        source = Mock()
        input = Mock()

        module_path = 'simphony_paraview.core.compatibility.VTK_VERSION'
        with patch(module_path) as VTK_VERSION:
            VTK_VERSION.__getitem__ = lambda x, y: version[y]
            with self.assertRaises(RuntimeError):
                set_input(source, input)
