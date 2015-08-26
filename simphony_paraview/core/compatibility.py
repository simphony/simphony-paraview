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
        vtkInteractorStyleSwitch)
elif paraview_major == 4:
    from vtk import (
        vtkUnstructuredGridWriter,
        vtkStructuredPointsWriter,
        vtkPolyDataWriter,
        vtkRenderWindowInteractor,
        vtkInteractorStyleSwitch)
else:
    message = 'Cannot work work with paraview {}'.format(paraview_major)
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
    'vtkInteractorStyleSwitch']
