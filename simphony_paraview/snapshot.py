from paraview.simple import Glyph, Sphere
from paraview.servermanager import CreateRenderView
from simphony.cuds import ABCMesh, ABCLattice, ABCParticles


from simphony_paraview.core.api import (
    loaded_in_paraview, typical_distance, set_data)
from simphony_paraview.core.fixes import CreateRepresentation


def snapshot(cuds, filename, select=None):
    """ Save a snapshot of the cuds object using the default visualisation.

     Parameters
     ----------
     cuds :
         A top level cuds object (e.g. a mesh). The method will detect
         the type of object and create the appropriate visualisation.

     filename : string
         The filename to use for the output file.

     select : tuple(CUBA, kind)
         The (CUBA, kind) selection of the CUBA attribute to
         use. ``kind`` can be one of the {'point', 'particles',
         'nodes', 'elements', 'bonds'}

    """
    with loaded_in_paraview(cuds) as source:

        # XXX Special workaround to avoid segfault on exit as
        # as seen in http://www.paraview.org/Bug/view.php?id=13124

        view = CreateRenderView()
        view.UseOffscreenRendering = 1
        view.UseOffscreenRenderingForScreenshots = 1

        representation = CreateRepresentation(source, view)

        items = None if select is None else select[1]
        message = "Container does not have: {}"
        if isinstance(cuds, ABCLattice):
            representation.Representation = "Points"
            if items not in (None, 'nodes'):
                raise ValueError(message.format(items))
        elif isinstance(cuds, ABCParticles):
            sphere = Sphere(Radius=typical_distance(source))
            glyphs = Glyph(Input=source, ScaleMode='off', GlyphType=sphere)
            representation = CreateRepresentation(glyphs, view)
            if items not in (None, 'particles', 'bonds'):
                raise ValueError(message.format(items))
        elif isinstance(cuds, ABCMesh):
            representation.Representation = "Surface"
            if items not in (None, 'points', 'elements'):
                raise ValueError(message.format(items))

        if select is not None:
            set_data(representation, source, select)

        view.ViewSize = [800, 600]
        view.Background = (0.2, 0.2, 0.2)
        view.ResetCamera()
        camera = view.GetActiveCamera()
        camera.Elevation(45)
        camera.Yaw(45)
        view.ResetCamera()
        view.WriteImage(filename, "vtkPNGWriter", 1)
