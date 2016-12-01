import numpy

from simphony.cuds.lattice import make_cubic_lattice
from simphony.core.cuba import CUBA

lattice = make_cubic_lattice('test', 0.1, (50, 10, 120))


def set_temperature(nodes):
    for node in nodes:
        index = numpy.array(node.index) + 1.0
        node.data[CUBA.TEMPERATURE] = numpy.prod(index)
        yield node


lattice.update_nodes(set_temperature(lattice.iter_nodes()))


if __name__ == '__main__':
    from simphony.visualisation import paraview_tools

    # Visualise the Lattice object
    paraview_tools.show(lattice, select=(CUBA.TEMPERATURE, 'nodes'))
