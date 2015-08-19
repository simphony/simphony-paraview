from paraview import servermanager
from paraview.servermanager import CreateProxy


def CreateRepresentation(aProxy, view, **extraArgs):
    """Creates a representation for the proxy and adds it to the render module.

    XXX Special workaround to avoid segfault on exit as as seen in
    http://www.paraview.org/Bug/view.php?id=13124.

    This method can also be used to initialize properties by passing
    keyword arguments where the key is the name of the property.In
    addition registrationGroup and registrationName (optional) can be
    specified (as keyword arguments) to automatically register the
    proxy with the proxy manager.

    This method tries to create the best possible representation for
    the given proxy in the given view. Additionally, the user can
    specify proxyName (optional) to create a representation of a
    particular type.


    """
    rendering = servermanager.rendering
    if not aProxy:
        raise RuntimeError("proxy argument cannot be None.")
    if not view:
        raise RuntimeError("view argument cannot be None.")
    if "proxyName" in extraArgs:
        display = CreateProxy("representations", extraArgs['proxyName'], None)
        del extraArgs['proxyName']
    else:
        display = view.SMProxy.CreateDefaultRepresentation(aProxy.SMProxy, 0)
        # XXX Special workaround to avoid segfault on exit as
        # as seen in http://www.paraview.org/Bug/view.php?id=13124
        # if display:
        #     display.UnRegister(None)
    if not display:
        return None
    extraArgs['proxy'] = display
    proxy = rendering.__dict__[display.GetXMLName()](**extraArgs)
    proxy.Input = aProxy
    proxy.UpdateVTKObjects()
    view.Representations.append(proxy)
    return proxy
