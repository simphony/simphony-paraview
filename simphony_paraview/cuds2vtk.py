from paraview import vtk

from simphony.cuds import ABCMesh, ABCParticles, ABCLattice


def cuds2vtk(cuds):
    """ Create a vtk.Dataset from a CUDS container """

    if isinstance(cuds, ABCMesh):
        data_set = vtk.vtkUnstructuredGrid()
    elif isinstance(cuds, ABCParticles):
        points = []
        lines = []
        particle2index = {}
        bond2index = {}
        index2particle = {}
        index2bond = {}
        data_set = vtk.vtkPolyData()
        for index, particle in enumerate(cuds.iter_particles()):
            uid = particle.uid
            particle2index[uid] = index
            index2particle[index] = uid
            points.append(particle.coordinates)
        for index, bond in enumerate(cuds.iter_bonds()):
            uid = bond.uid
            bond2index[uid] = index
            index2bond[index] = uid
            lines.append([particle2index[uuid] for uuid in bond.particles])
    elif isinstance(cuds, ABCLattice):
        data_set = vtk.vtkImageData()

    return data_set
