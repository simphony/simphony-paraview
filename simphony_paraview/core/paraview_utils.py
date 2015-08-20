import contextlib
import os
import tempfile
import shutil

import math

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


def typical_distance(source):
    """ Returns a typical distance in a cloud of points.

    This is done by taking the size of the bounding box, and dividing it
    by the cubic root of the number of points.

    .. note:: Code inspired from the Mayavi package.

    """
    source.UpdatePipeline()  #  Make sure that the bounds are uptodata
    info = source.GetDataInformation()
    x_min, x_max, y_min, y_max, z_min, z_max = info.GetBounds()
    distance = math.sqrt(
        (x_max - x_min) ** 2 + (y_max - y_min) ** 2 + (z_max - z_min) ** 2)
    distance /= info.GetNumberOfPoints()
    if distance == 0.0:
        return 1.0
    else:
        return 0.5 * distance


def set_data(representation, source, select):
    name = select[0].name
    if select[1] in ('points', 'particles', 'nodes'):
        array = source.PointData[name]
        representation.LookupTable = MakeBlueToRedLT(*array.GetRange())
        representation.ColorAttributeType = 'POINT_DATA'
    elif select[1] in ('elements', 'bonds'):
        array = source.CellData[name]
        representation.LookupTable = MakeBlueToRedLT(*array.GetRange())
        representation.ColorAttributeType = 'CELL_DATA'
    else:
        message = "Unknown data attribute selection {}"
        raise ValueError(message.format(select[1]))
    representation.ColorArrayName = name
