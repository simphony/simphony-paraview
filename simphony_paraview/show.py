from paraview.simple import Glyph, Sphere
from paraview import servermanager
from paraview.servermanager import CreateRenderView
from vtkRenderingPython import (
    vtkRenderWindowInteractor, vtkInteractorStyleSwitch)
from simphony.cuds import ABCMesh, ABCLattice, ABCParticles

from simphony_paraview.core.api import (
    loaded_in_paraview, typical_distance, set_data)
from simphony_paraview.core.fixes import CreateRepresentation


def show(cuds, select=None, testing=None):
    """ Show the cuds objects using the default visualisation.

     Parameters
     ----------
     cuds : {ABCLattice, ABCMesh, ABCParticles}
         A top level cuds object (e.g. a mesh). The method will detect
         the type of object and create the appropriate visualisation.
     testing : callable(obj, event)
         A callable object that accepts an the interactor object and a
         time event. The callable will be executed after 1000 msec.
         This is commonly used for testing. Default value is None

    """
    with loaded_in_paraview(cuds) as source:

        # XXX Special workaround to avoid segfault on exit as
        # as seen in http://www.paraview.org/Bug/view.php?id=13124

        view = CreateRenderView()
        view.ResetCamera()
        camera = view.GetActiveCamera()
        camera.Elevation(45)

        representation = CreateRepresentation(source, view)

        if isinstance(cuds, ABCLattice):
            representation.Representation = "Points"
            if select is not None:
                set_data(representation, source, select)
        elif isinstance(cuds, ABCParticles):
            sphere = Sphere(Radius=typical_distance(source))
            glyphs = Glyph(Input=source, ScaleMode='off', GlyphType=sphere)
            glyph_representation = CreateRepresentation(glyphs, view)
            if select is not None:
                if select[1] == 'particles':
                    set_data(glyph_representation, source, select)
                else:
                    set_data(representation, source, select)
        elif isinstance(cuds, ABCMesh):
            representation.Representation = "Surface"
            if select is not None:
                set_data(representation, source, select)

        interactor = vtkRenderWindowInteractor()
        interactor.SetInteractorStyle(vtkInteractorStyleSwitch())
        interactor.SetRenderWindow(view.GetRenderWindow())
        interactor.Initialize()

        if testing is not None:
            timerid = interactor.CreateOneShotTimer(1000)
            handler = Handler(testing, timerid)
            interactor.AddObserver('TimerEvent', handler)
        try:
            view.StillRender()
            interactor.Start()
        finally:
            interactor.RemoveAllObservers()


class Handler(object):

    def __init__(self, callback, timerid):
        self.callback = callback
        self.timerid = timerid

    def __call__(self, obj, event):
        self.callback(obj, event)
        obj.DestroyTimer(self.timerid)
