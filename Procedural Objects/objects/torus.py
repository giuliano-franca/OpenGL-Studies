# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

====================================================================================================

How to use:
    * Install Python 3. (I'm using Python 3.7.4)
    * Pip install all the dependencies.
    * Run the file.

Dependencies:
    * Python 3
    * PyOpenGL
    * GLFW
    * PySide2
    * Numpy

Todo:
    * TODO(slider): Update slider values.

Sources:
    * NDA

This code supports Pylint. Rc file in project.
"""
import math
import collections
import numpy as np
import OpenGL.GL as gl
from PySide2 import QtCore
from PySide2 import QtUiTools


class ProceduralTorus(QtCore.QObject):
    """Class of the torus parameters."""

    def __init__(self, file, glViewer, parent=None):
        super(ProceduralTorus, self).__init__(parent)
        loader = QtUiTools.QUiLoader()
        torusUIFile = QtCore.QFile(file)
        torusUIFile.open(QtCore.QFile.ReadOnly)
        self.widget = loader.load(torusUIFile)
        self.glViewer = glViewer
        torusUIFile.close()

        self._radius = 10
        self._secRadius = 5
        self._twist = 0
        self._subdAxis = 10
        self._subdHeight = 10

        self.restoreDefaults()
        self.configureWidgets()

    def configureWidgets(self):
        """Configure all widgets."""
        self.widget.sld_radius.sliderMoved.connect(self.updateAllValues)
        self.widget.sld_secRadius.sliderMoved.connect(self.updateAllValues)
        self.widget.sld_twist.sliderMoved.connect(self.updateAllValues)
        self.widget.sld_subdAxis.sliderMoved.connect(self.updateAllValues)
        self.widget.sld_subdHeight.sliderMoved.connect(self.updateAllValues)

    def updateAllValues(self):
        """Update all values from the sliders to the instance."""
        radiusVal = self.widget.sld_radius.value()
        secRadiusVal = self.widget.sld_secRadius.value()
        twistVal = self.widget.sld_twist.value()
        subdAxisVal = self.widget.sld_subdAxis.value()
        subdHeightVal = self.widget.sld_subdHeight.value()
        self._radius = radiusVal
        self._secRadius = secRadiusVal
        self._twist = twistVal
        self._subdAxis = subdAxisVal
        self._subdHeight = subdHeightVal
        self.glViewer.update()

    def restoreDefaults(self):
        """Restores widgets to default value."""
        self.widget.sld_radius.setValue(10)
        self.widget.sld_secRadius.setValue(5)
        self.widget.sld_twist.setValue(0)
        self.widget.sld_subdAxis.setValue(10)
        self.widget.sld_subdHeight.setValue(10)
        self.updateAllValues()

    @property
    def torusRadius(self):
        """Return the radius of the torus.

        Returns:
            float: The radius value of the torus.
        """
        return self._radius * 0.1

    @property
    def torusSecRadius(self):
        """Return the section radius of the torus.

        Returns:
            float: The section radius value of the torus.
        """
        return self._secRadius * 0.1

    @property
    def torusTwist(self):
        """Return the twist of the torus.

        Returns:
            int: The twist value of the torus.
        """
        return self._twist

    @property
    def torusSubdAxis(self):
        """Return the subdivisions axis of the torus.

        Returns:
            int: The subdivisions axis value of the torus.
        """
        return self._subdAxis

    @property
    def torusSubdHeight(self):
        """Return the subdivisions height of the torus.

        Returns:
            int: The subdivisions height value of the torus.
        """
        return self._subdHeight

    def draw(self):
        """Draw a torus using OpenGL functions."""
        # pylint: disable=unused-variable
        subdAxis = self.torusSubdAxis
        subdHeight = self.torusSubdHeight
        radius = self.torusRadius
        secRadius = self.torusSecRadius
        twist = self.torusTwist

        step = 2.0 * math.pi / subdAxis
        stepSec = 2.0 * math.pi / subdHeight
        loops = collections.OrderedDict()
        gl.glColor3f(1.0, 0.0, 0.0)
        gl.glPointSize(6.0)
        gl.glBegin(gl.GL_POINTS)
        for i in range(subdAxis):
            alpha = step * i + (math.pi / 2.0)
            mOrigin = np.identity(4)
            mOrigin[0][0] = math.cos(-alpha)
            mOrigin[0][2] = -math.sin(-alpha)
            mOrigin[2][0] = math.sin(-alpha)
            mOrigin[2][2] = math.cos(-alpha)
            mOrigin[3][0] = math.cos(step * i) * radius
            mOrigin[3][2] = math.sin(step * i) * radius
            gl.glVertex3f(mOrigin[3][0], mOrigin[3][1], mOrigin[3][2])
        gl.glEnd()
