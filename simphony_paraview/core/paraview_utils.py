import contextlib
import os
import tempfile
import shutil

from paraview import servermanager
from paraview.simple import Disconnect, Connect, Delete, OpenDataFile

from paraview import vtk
from paraview.vtk import io

from .cuds2vtk import cuds2vtk
from .constants import dataset2writer


def running_in_paraview():
    return servermanager.fromGUI


@contextlib.contextmanager
def loadded_in_paraview(cuds):
    """ Push dataset to the Paraview server.

    The context manager will create a connection if necessary and


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
    data_set = cuds2vtk(cuds)
    kind = data_set.GetDataObjectType()
    writer = dataset2writer()[kind]()
    writer.SetFileName(filename)
    writer.SetInput(data_set)
    writer.Write()
