SimPhoNy
========


Paraview tools are available in the simphony library through the
visualisation plug-in named ``paraview_tools``.

e.g::

  from simphony.visualisation import paraview_tools

Visualizing CUDS
----------------

The :func:`~simphony_paraview.show.show` function is available to
visualise any top level CUDS container. The function will open a
window containing a 3D view of the dataset. Interaction is supported
using the mouse and keyboard:

:keyboard:
  - :kbd:`j` / :kbd:`t`: toggle between joystick (position sensitive) and
    trackball (motion sensitive) styles. In joystick style, motion
    occurs continuously as long as a mouse button is pressed. In
    trackball style, motion occurs when the mouse button is pressed
    and the mouse pointer moves.

  - :kbd:`3`: toggle the render window into and out of stereo mode. By
    default, red-blue stereo pairs are created.

  - :kbd:`e`: exit the application.

  - :kbd:`f`: fly to the picked point

  - :kbd:`p`: perform a pick operation.

  - :kbd:`r`: reset the camera view along the current view
    direction. Centers the actors and moves the camera so that all
    actors are visible.

  - :kbd:`s`: modify the representation of all actors so that they are
    surfaces.

  - :kbd:`w`: modify the representation of all actors so that they are
    wireframe.

:mouse:
  - **Button 1**: rotate the camera around its focal point (if camera
    mode) or rotate the actor around its origin (if actor mode). The
    rotation is in the direction defined from the center of the
    renderer's viewport towards the mouse position. In joystick mode,
    the magnitude of the rotation is determined by the distance the
    mouse is from the center of the render window.

  - **Button 2**: pan the camera (if camera mode) or translate the
    actor (if actor mode). In joystick mode, the direction of pan or
    translation is from the center of the viewport towards the mouse
    position. In trackball mode, the direction of motion is the
    direction the mouse moves. (Note: with 2-button mice, pan is
    defined as <Shift>-Button 1.)

  - **Button 3**: zoom the camera (if camera mode) or scale the actor (if
    actor mode). Zoom in/increase scale if the mouse position is in
    the top half of the viewport; zoom out/decrease scale if the mouse
    position is in the bottom half. In joystick mode, the amount of
    zoom is controlled by the distance of the mouse pointer from the
    horizontal centerline of the window.

.. rubric:: Mesh example

.. literalinclude:: ../../examples/mesh_example.py

.. figure:: _images/mesh_show.png

.. rubric:: Lattice example

.. literalinclude:: ../../examples/lattice_example.py

.. figure:: _images/lattice_show.png

.. rubric:: Particles example

.. literalinclude:: ../../examples/particles_example.py

.. figure:: _images/particles_show.png
