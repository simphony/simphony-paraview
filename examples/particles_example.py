from numpy import array

from simphony.cuds import Particles, Particle, Bond
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA


points = array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]], 'f')
bonds = array([[0, 1], [0, 3], [1, 3, 2]])
temperature = array([10., 20., 30., 40.])

particles = Particles('test')
uids = particles.add_particles(
    Particle(
        coordinates=point,
        data=DataContainer(TEMPERATURE=temperature[index]))
    for index, point in enumerate(points))

particles.add_bonds(
    Bond(particles=[uids[index] for index in indices])
    for indices in bonds)


if __name__ == '__main__':
    from simphony.visualisation import paraview_tools

    # Visualise the Particles object
    paraview_tools.show(particles, select=(CUBA.TEMPERATURE, 'particles'))
