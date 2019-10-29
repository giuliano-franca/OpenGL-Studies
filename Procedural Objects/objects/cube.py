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
    * NDA

Sources:
    * https://www.desmos.com/calculator/4u5eih39bk

This code supports Pylint. Rc file in project.
"""
import math
import collections
import numpy as np
import OpenGL.GL as gl
from PySide2 import QtCore
from PySide2 import QtUiTools


class ProceduralCube(QtCore.QObject):
    """Class of the cube parameters."""

    def __init__(self, file, glViewer, parent=None):
        super(ProceduralCube, self).__init__(parent)
        loader = QtUiTools.QUiLoader()
        cubeUIFile = QtCore.QFile(file)
        cubeUIFile.open(QtCore.QFile.ReadOnly)
        self.widget = loader.load(cubeUIFile)
        self.glViewer = glViewer
        cubeUIFile.close()

        self._width = 10
        self._height = 10
        self._depth = 10
        self._subdWidth = 1
        self._subdHeight = 1
        self._subdDepth = 1

        self.restoreDefaults()
        self.configureWidgets()

    def configureWidgets(self):
        """Configure all widgets."""
        self.widget.sld_width.sliderMoved.connect(self.updateAllValues)
        self.widget.sld_height.sliderMoved.connect(self.updateAllValues)
        self.widget.sld_depth.sliderMoved.connect(self.updateAllValues)
        self.widget.sld_subdWidth.sliderMoved.connect(self.updateAllValues)
        self.widget.sld_subdHeight.sliderMoved.connect(self.updateAllValues)
        self.widget.sld_subdDepth.sliderMoved.connect(self.updateAllValues)

    def updateAllValues(self):
        """Update all values from the sliders to the instance."""
        widthVal = self.widget.sld_width.value()
        heightVal = self.widget.sld_height.value()
        depthVal = self.widget.sld_depth.value()
        subdWidthVal = self.widget.sld_subdWidth.value()
        subdHeightVal = self.widget.sld_subdHeight.value()
        subdDepthVal = self.widget.sld_subdDepth.value()
        self._width = widthVal
        self._height = heightVal
        self._depth = depthVal
        self._subdWidth = subdWidthVal
        self._subdHeight = subdHeightVal
        self._subdDepth = subdDepthVal
        self.glViewer.update()

    def restoreDefaults(self):
        """Restores widgets to default value."""
        self.widget.sld_width.setValue(10)
        self.widget.sld_height.setValue(10)
        self.widget.sld_depth.setValue(10)
        self.widget.sld_subdWidth.setValue(1)
        self.widget.sld_subdHeight.setValue(1)
        self.widget.sld_subdDepth.setValue(1)
        self.updateAllValues()

    @property
    def cubeWidth(self):
        """Return the width of the cube.

        Returns:
            float: The width value of the cube.
        """
        return self._width * 0.1

    @property
    def cubeHeight(self):
        """Return the height of the cube.

        Returns:
            float: The height value of the cube.
        """
        return self._height * 0.1

    @property
    def cubeDepth(self):
        """Return the depth of the cube.

        Returns:
            float: The depth value of the cube.
        """
        return self._depth * 0.1

    @property
    def cubeSubdWidth(self):
        """Return the subdivisions width of the cube.

        Returns:
            float: The subdivisions width value of the cube.
        """
        return self._subdWidth

    @property
    def cubeSubdHeight(self):
        """Return the subdivisions height of the cube.

        Returns:
            float: The subdivisions height value of the cube.
        """
        return self._subdHeight

    @property
    def cubeSubdDepth(self):
        """Return the subdivisions depth of the cube.

        Returns:
            float: The subdivisions depth value of the cube.
        """
        return self._subdDepth

    def draw(self):
        """Draw a cube using OpenGL functions."""
        # pylint: disable=unused-variable
        width = self.cubeWidth
        height = self.cubeHeight
        depth = self.cubeDepth
        subdWidth = self.cubeSubdWidth
        subdHeight = self.cubeSubdHeight
        subdDepth = self.cubeSubdDepth

        stepW = 1 / subdWidth
        stepH = 1 / subdHeight
        stepD = 1 / subdDepth

        vtxList = []

        gl.glColor3f(1.0, 0.0, 0.0)
        gl.glPointSize(6.0)
        gl.glBegin(gl.GL_POINTS)
        gl.glVertex3f(width, height, depth)
        gl.glVertex3f(-width, height, depth)
        gl.glVertex3f(width, -height, depth)
        gl.glVertex3f(-width, -height, depth)
        gl.glVertex3f(width, -height, -depth)
        gl.glVertex3f(-width, -height, -depth)
        gl.glVertex3f(width, height, -depth)
        gl.glVertex3f(-width, height, -depth)
        gl.glEnd()
