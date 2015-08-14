import contextlib
import os
import tempfile
import shutil

from paraview import servermanager
from paraview.simple import Disconnect, Connect, Delete, OpenDataFile

from .cuds2vtk import cuds2vtk
from .constants import dataset2writer


@contextlib.contextmanager
def loaded_in_paraview(cuds):
    """ Push cuds dataset to the Paraview server.

    The context manager will create a connection if necessary and save the
    data of the cuds container into a vtk file. The vtk file is then loaded
    in the paraview server and a proxy source is returned.

    """
    temp_dir = tempfile.mkdtemp(prefix='simphony-')
    filename = os.path.join(temp_dir, 'temp_cuds.vtk')
    source = None
    if servermanager.ActiveConnection is None:
        connection = Connect()
    else:
        connection = None
    try:
        write_to_file(cuds, filename)
        source = OpenDataFile(filename)
        yield source
    finally:
        if source is not None:
            Delete(source)
        if connection is not None:
            Disconnect()
        shutil.rmtree(temp_dir)


def write_to_file(cuds, filename):
    """ Write a cuds container into a vtk file. """
    data_set = cuds2vtk(cuds)
    kind = data_set.GetDataObjectType()
    writer = dataset2writer()[kind]()
    writer.SetFileName(filename)
    writer.SetInput(data_set)
    writer.Write()
