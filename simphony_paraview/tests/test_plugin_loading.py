import unittest


class TestPluginLoading(unittest.TestCase):

    def test_import(self):
        try:
            from simphony.visualisation import paraview_tools  # noqa
        except ImportError:
            self.fail('Could not import the paraview visualisation')

    def test_function_api(self):

        from simphony.visualisation import paraview_tools

        self.assertTrue(hasattr(paraview_tools, '__version__'))
