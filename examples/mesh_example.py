from numpy import array

from simphony.cuds import Mesh, Point, Cell, Edge, Face
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA


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
edge_uids = mesh.add_edges(
    Edge(points=[uids[index] for index in element])
    for index, element in enumerate(edges))

# add faces
face_uids = mesh.add_faces(
    Face(points=[uids[index] for index in element])
    for index, element in enumerate(faces))

# add cells
cell_uids = mesh.add_cells(
    Cell(points=[uids[index] for index in element])
    for index, element in enumerate(cells))

if __name__ == '__main__':
    from simphony.visualisation import paraview_tools

    # Visualise the Mesh object
    paraview_tools.show(mesh, select=(CUBA.TEMPERATURE, 'points'))
