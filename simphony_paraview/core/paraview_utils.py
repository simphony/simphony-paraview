import contextlib
import os
import tempfile
import shutil

from paraview import servermanager
from paraview.simple import (
    Disconnect, Connect, Delete, OpenDataFile, MakeBlueToRedLT)

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


def set_data(representation, source, select):
    name = select[0].name
    if select[1] in ('points', 'particles', 'nodes'):
        array = source.PointData[name]
        representation.LookupTable = MakeBlueToRedLT(*array.GetRange())
        representation.ColorAttributeType = 'POINT_DATA'
    else:
        array = source.CellData[name]
        representation.LookupTable = MakeBlueToRedLT(*array.GetRange())
        representation.ColorAttributeType = 'CELL_DATA'
    representation.ColorArrayName = name
