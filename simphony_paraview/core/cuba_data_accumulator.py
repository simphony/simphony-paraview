import logging

import numpy
from paraview import vtk
from paraview.numpy_support import get_vtk_array_type, create_vtk_array
from simphony.core.cuba import CUBA

from .cuba_utils import (
    supported_cuba, cuba_value_types, default_cuba_value, VALUETYPES)


logger = logging.getLogger(__name__)


class CUBADataAccumulator(object):
    """ Accumulate data information per CUBA key.

    A collector object that stores :class:``DataContainer`` data into
    a vtkPointData or vtkCellData array containers where each CUBA key
    is an array.  instanced the user can effectively convert the per
    item mapping of data values in a CUDS container to a per CUBA key
    mapping of the data values of a vtk array container.

    The Accumulator has two modes of operation ``fixed`` and
    ``expand``. ``fixed`` means that data will be stored for
    a predefined set of keys on every ``append`` call and missing
    values will be saved as ``None``. Where ``expand`` will extend
    the internal table of values whenever a new key is introduced.

    .. rubric:: expand operation

    >>> accumulator = CUBADataAccumulator():
    >>> accumulator.append(DataContainer(TEMPERATURE=34))
    >>> accumulator.keys()
    {CUBA.TEMPERATURE}
    >>> accumulator.append(DataContainer(VELOCITY=(0.1, 0.1, 0.1))
    >>> accumulator.append(DataContainer(TEMPERATURE=56))
    >>> accumulator.keys()
    {CUBA.TEMPERATURE, CUBA.VELOCITY}
    >>> accumulator[CUBA.TEMPERATURE]
    [34, None, 56]
    >>> accumulator[CUBA.VELOCITY]
    [None, (0.1, 0.1, 0.1), None]

    .. rubric:: fixed operation

    >>> accumulator = CUBADataAccumulator([CUBA.TEMPERATURE, CUBA.PRESSURE]):
    >>> accumulator.keys()
    {CUBA.TEMPERATURE, CUBA.PRESSURE}
    >>> accumulator.append(DataContainer(TEMPERATURE=34))
    >>> accumulator.append(DataContainer(VELOCITY=(0.1, 0.1, 0.1))
    >>> accumulator.append(DataContainer(TEMPERATURE=56))
    >>> accumulator.keys()
    {CUBA.TEMPERATURE, CUBA.PRESSURE}
    >>> accumulator[CUBA.TEMPERATURE]
    [34, None, 56]
    >>> accumulator[CUBA.PRESSURE]
    [None, None, None]
    >>> accumulator[CUBA.VELOCITY]
    KeyError(...)

    """
    def __init__(self, keys=(), container=None):
        """Constructor

        Parameters
        ----------
        keys : list

            The list of keys that the accumulator should care
            about. Providing this value at initialisation sets up the
            accumulator to operate in ``fixed`` mode. If no keys are
            provided then accumulator operates in ``expand`` mode.

        """
        self.data = vtk.vtkPointData() if container is None else container
        self._cuba_types = cuba_value_types()
        self._number_of_items = 0
        if len(keys) > 0:
            self._keys = set(keys) & supported_cuba()
            self._expand(self._keys)
        else:
            self._keys = supported_cuba()
        self._expand_mode = len(keys) == 0
        self._cubas = None

    @property
    def keys(self):
        """ The set of CUBA keys that this accumulator contains.

        """
        if self._cubas is None:
            data = self.data
            self._cubas = set(
                CUBA[data.GetArray(index).GetName()]
                for index in range(data.GetNumberOfArrays()))
        return set(self._cubas)

    def append(self, data):
        """ Append info from a ``DataContainer``.

        Parameters
        ----------
        data : DataContainer
            The data information to append.

        If the accumulator operates in ``fixed`` mode:

        - Any keys in :code:`self.keys()` that have values in ``data``
          will be stored (appended to the related key lits).
        - Missing keys will be stored as ``None``

        If the accumulator operates in ``expand`` mode:

        - Any new keys in `Data` will be added to the :code:`self.keys()` list
          and the related list of values with length equal to the current
          record size will be initialised with values of ``None``.
        - Any keys in the modified :code:`self.keys()` that have values in
          ``data`` will be stored (appended to the list of the related key).
        - Missing keys will be store as ``None``.

        """
        if self._expand_mode:
            new_keys = set(data.keys()) - self.keys & self._keys
            self._expand(new_keys)
            self._cubas = None
        self._append(data)
        self._number_of_items += 1

    def __len__(self):
        """ The number of values that are stored per key

        """
        return self._number_of_items

    def __getitem__(self, key):
        """ Get the list of accumulated values for the CUBA key.

        Parameters
        ----------
        key : CUBA
            A CUBA Enum value

        Returns
        -------
        result : vtkDataArray
            An array of data values collected for ``key``. Missing values
            are designated with the default value as returned by
            :function:`~.dummy_cuba_value`.

        """
        container = self.data
        return container.GetArray(key.name)

    def _expand(self, cubas):
        size = len(self)
        for cuba in cubas:
            default = default_cuba_value(cuba)
            temp = numpy.asarray(default)
            vtk_type = get_vtk_array_type(temp.dtype)
            array = create_vtk_array(vtk_type)
            array.SetNumberOfComponents(temp.size)
            array.SetNumberOfTuples(size)
            array.SetName(cuba.name)
            for index, value in enumerate(temp.ravel()):
                array.FillComponent(index, value)
            self.data.AddArray(array)

    def _append(self, data):
        for cuba in self.keys:
            default = default_cuba_value(cuba)
            array = self[cuba]
            value = data.get(cuba, default)
            value_type = self._cuba_types[cuba]
            if value_type == VALUETYPES.SCALAR:
                array.InsertNextValue(value)
            elif value_type == VALUETYPES.VECTOR:
                array.InsertNextTuple(value.ravel())
