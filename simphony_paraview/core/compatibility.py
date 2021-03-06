from paraview import servermanager
from paraview.vtk import VTK_VERSION

paraview_major = servermanager.vtkSMProxyManager.GetVersionMajor()

if paraview_major == 3:
    from paraview.vtk.io import (
        vtkUnstructuredGridWriter,
        vtkStructuredPointsWriter,
        vtkPolyDataWriter)
    from vtkRenderingPython import (
        vtkRenderWindowInteractor,
        vtkInteractorStyleJoystickCamera)
elif paraview_major == 4:
    # Paraview 4 ships with vtk6.
    # Make sure that PYTHONPATH points to the correct path
    # for binary modules (e.g. /usr/lib/paraview/).
    from vtkIOLegacyPython import (
        vtkUnstructuredGridWriter,
        vtkStructuredPointsWriter,
        vtkPolyDataWriter)
    from vtkRenderingCorePython import (
        vtkRenderWindowInteractor)
    from vtkInteractionStylePython import (
        vtkInteractorStyleJoystickCamera)
else:
    message = 'Cannot work with paraview {}'.format(paraview_major)
    raise ImportError(message)


def set_input(source, input):
    major = int(VTK_VERSION[0])
    if major == 6:
        source.SetInputData(input)
    elif major == 5:
        source.SetInput(input)
    else:
        message = 'Cannot work work with vtk {}'.format(VTK_VERSION)
        raise RuntimeError(message)


__all__ = [
    'vtkUnstructuredGridWriter',
    'vtkStructuredPointsWriter',
    'vtkPolyDataWriter',
    'vtkRenderWindowInteractor',
    'vtkInteractorStyleJoystickCamera']
