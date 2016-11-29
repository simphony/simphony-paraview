# -*- coding: utf-8 -*-
#
# SimPhoNy-Mayavi documentation build configuration file
#
import sys


def mock_modules():
    MOCK_MODULES = []
    MOCK_TYPES = []

    try:
        import paraview  # noqa
    except ImportError:
        MOCK_MODULES.extend((
            'paraview',
            'paraview.simple',
            'paraview.servermanager',
            'paraview.numpy_support',
            'paraview.vtk',
            'vtkRenderingPython'))

    TYPES = {
        mock_type: type(mock_type, bases, {'__module__': path})
        for path, mock_type, bases in MOCK_TYPES}

    class DocMock(object):

        def __init__(self, *args, **kwds):
            if '__doc_mocked_name__' in kwds:
                self.__docmock_name__ = kwds['__docmocked_name__']
            else:
                self.__docmock_name__ = 'Unknown'

        def __getattr__(self, name):
            if name in ('__file__', '__path__'):
                return '/dev/null'
            else:
                return TYPES.get(name, DocMock(__docmock_name__=name))

        def __call__(self, *args, **kwards):
            return DocMock()

        @property
        def __name__(self):
            return self.__docmock_name__

        def __repr__(self):
            return '<DocMock.{}>'.format(self.__name__)

    sys.modules.update(
        (mod_name, DocMock(mocked_name=mod_name)) for mod_name in MOCK_MODULES)
    print 'mocking modules {} and types {}'.format(MOCK_MODULES, MOCK_TYPES)


# -- General configuration ------------------------------------------------
# check and mock missing modules
mock_modules()

# import the release and version value from the module
from simphony_paraview._version import full_version, version  # noqa

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sectiondoc.styles.legacy']

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'SimPhoNy-Paraview'
copyright = u'2015, SimPhoNy FP7 Collaboration'
pygments_style = 'sphinx'
autoclass_content = 'both'
release = version
version = full_version

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'http://docs.python.org/': None}

# -- Options for HTML output ----------------------------------------------

html_theme = 'alabaster'
html_logo = '_static/simphony_logo.png'
html_static_path = ['_static']
htmlhelp_basename = 'SimPhoNy-ParaviewDoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {}
latex_documents = [(
    'index', 'SimPhoNy-Mayavi.tex', u'SimPhoNy-Mayavi Documentation',
    u'SimPhoNy FP7 Collaboration', 'manual')]
latex_logo = '_static/simphony_logo.png'

# -- Options for manual page output ---------------------------------------

man_pages = [(
    'index', 'simphony', u'SimPhoNy-Mayavi Documentation',
    [u'SimPhoNy FP7 Collaboration'], 1)]

# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [(
    'index', 'SimPhoNy', u'SimPhoNy-Paraview Documentation',
    u'SimPhoNy FP7 Collaboration', 'SimPhoNy-Paraview', 'Visualisation tools',
    'Miscellaneous'),
]

# -- Options for Epub output ----------------------------------------------

epub_title = u'SimPhoNy-Paraview'
epub_author = u'SimPhoNy FP7 Collaboration'
epub_publisher = u'SimPhoNy FP7 Collaboration'
epub_copyright = u'2015, SimPhoNy FP7 Collaboration'
epub_exclude_files = ['search.html']
