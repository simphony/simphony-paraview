from numpy import array, prod

from hypothesis.strategies import sampled_from
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from simphony.cuds import (
    Mesh, Point, Cell, Edge, Face, Particles, Particle, Bond)
from simphony.cuds.lattice import make_cubic_lattice


def create_example_lattice():
    lattice = make_cubic_lattice('test', 0.1, (5, 10, 12))

    def work_on_nodes(nodes):
        for node in nodes:
            index = array(node.index) + 1.0
            node.data[CUBA.TEMPERATURE] = prod(index)
            yield node

    lattice.update_nodes(work_on_nodes(lattice.iter_nodes()))
    return lattice


def create_example_mesh():
    points = array([
        [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
        [2, 0, 0], [3, 0, 0], [3, 1, 0], [2, 1, 0],
        [2, 0, 1], [3, 0, 1], [3, 1, 1], [2, 1, 1]],
        'f')

    cells = [
        [0, 1, 2, 3],  # tetra
        [4, 5, 6, 7, 8, 9, 10, 11]]  # hex

    faces = [[2, 7, 11]]
    edges = [[1, 4], [3, 8]]

    mesh = Mesh('example')

    # add points
    uids = mesh.add_points(
        Point(coordinates=point, data=DataContainer(TEMPERATURE=index))
        for index, point in enumerate(points))

    # add edges
    mesh.add_edges(
        Edge(points=[uids[index] for index in element])
        for index, element in enumerate(edges))

    # add faces
    mesh.add_faces(
        Face(points=[uids[index] for index in element])
        for index, element in enumerate(faces))

    # add cells
    mesh.add_cells(
        Cell(points=[uids[index] for index in element])
        for index, element in enumerate(cells))

    return mesh


def create_example_particles():
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

    return particles


cuds_containers = sampled_from([
    (create_example_mesh(array_name='TEMPERATURE'), 'mesh'),
    (create_example_lattice(array_name='TEMPERATURE'), 'lattice-3d'),
    (create_example_particles(array_name='TEMPERATURE'), 'particles')])
