import warnings

import numpy
from simphony.core.cuba import CUBA
from simphony.core.keywords import KEYWORDS


def supported_cuba():
    """ Return a set of currently supported CUBA keys. """
    supported = set()
    message = 'property {} is currently ignored'
    for cuba in CUBA:
        default = default_cuba_value(cuba)
        if isinstance(default, (float, int, long)):
            supported.add(cuba)
        elif isinstance(default, numpy.ndarray):
            if default.ndim > 2:
                warnings.warn(message.format(cuba.name))
            else:
                supported.add(cuba)
        else:
            warnings.warn(message.format(cuba.name))
    return supported


def default_cuba_value(cuba):
    """ Return the default value of the CUBA key as a scalar or numpy array.

    Int type values have ``-1`` as default, while float type values
    have ``numpy.nan``.

    """
    description = KEYWORDS[cuba.name]

    if description.dtype is None:
        message = 'property {!r} is currently ignored'
        warnings.warn(message.format(cuba))
        return

    if description.shape == [1]:
        if numpy.issubdtype(description.dtype, numpy.float):
            return numpy.nan
        elif numpy.issubdtype(description.dtype, numpy.int):
            return -1
        else:
            message = 'property {!r} is currently ignored'
            warnings.warn(message.format(cuba))
    elif description.shape == [3]:
        if numpy.issubdtype(description.dtype, numpy.float):
            return numpy.array(
                [numpy.nan, numpy.nan, numpy.nan], dtype=description.dtype)
        elif numpy.issubdtype(description.dtype, numpy.int):
            return numpy.array([-1, -1, -1], dtype=description.dtype)
        else:
            message = 'property {!r} is currently ignored'
            warnings.warn(message.format(cuba))
    elif description.shape == [3, 3]:
        if numpy.issubdtype(description.dtype, numpy.float):
            return numpy.array([
                [numpy.nan, numpy.nan, numpy.nan],
                [numpy.nan, numpy.nan, numpy.nan],
                [numpy.nan, numpy.nan, numpy.nan]], dtype=description.dtype)
        elif numpy.issubdtype(description.dtype, numpy.int):
            return numpy.array(
                [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]],
                dtype=description.dtype)
        else:
            message = 'property {!r} is currently ignored'
            warnings.warn(message.format(cuba))
    elif description.dtype == numpy.str:
        return " " * description.shape[0]
    else:
        message = 'property {!r} is currently ignored'
        warnings.warn(message.format(cuba))
