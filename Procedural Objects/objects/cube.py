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
    * PySide2
    * Numpy

Todo:
    * NDA

Sources:
    * NDA

This code supports Pylint. Rc file in project.
"""
from PySide2 import QtCore
from PySide2 import QtUiTools


class ProceduralCube(QtCore.QObject):
    """Class of the cube parameters."""

    def __init__(self, file, parent=None):
        super(ProceduralCube, self).__init__(parent)
        loader = QtUiTools.QUiLoader()
        cubeUIFile = QtCore.QFile(file)
        cubeUIFile.open(QtCore.QFile.ReadOnly)
        self.widget = loader.load(cubeUIFile)
        cubeUIFile.close()

        self.widthDef = 10
        self.heightDef = 10
        self.depthDef = 10
        self.subdWidthDef = 1
        self.subdHeightDef = 1
        self.subdDepthDef = 1

        self.configureWidgets()

    def configureWidgets(self):
        """Configure all widgets."""
        self.widget.sld_width.setValue(self.widthDef)
        self.widget.sld_height.setValue(self.heightDef)
        self.widget.sld_depth.setValue(self.depthDef)
        self.widget.sld_subdWidth.setValue(self.subdWidthDef)
        self.widget.sld_subdHeight.setValue(self.subdHeightDef)
        self.widget.sld_subdDepth.setValue(self.subdDepthDef)

    def restoreDefaults(self):
        """Restores widgets to default value."""
        self.configureWidgets()

    @property
    def cubeWidth(self):
        """Return the width of the cube.

        Returns:
            float: The width value of the cube.
        """
        return self.widget.sld_width.value() * 0.1

    @property
    def cubeHeight(self):
        """Return the height of the cube.

        Returns:
            float: The height value of the cube.
        """
        return self.widget.sld_height.value() * 0.1

    @property
    def cubeDepth(self):
        """Return the depth of the cube.

        Returns:
            float: The depth value of the cube.
        """
        return self.widget.sld_depth.value() * 0.1

    def draw(self):
        """Draw a cube using OpenGL functions."""
        return None
