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
    * NDA

This code supports Pylint. Rc file in project.
"""
import sys
import OpenGL.GL as gl
import OpenGL.GLU as glu
import glfw
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtUiTools

from objects import cube
from objects import torus


class ProceduralObjects(QtCore.QObject):
    """Class of the main window."""

    @property
    def findCurrentProceduralObjectText(self):
        """Find the current selected procedural object text.

        Returns:
            str: The name of the current object.
        """
        return self.window.cmb_objType.currentText()

    @property
    def findCurrentProceduralObject(self):
        """Find the current selected procedural object.

        Returns:
            instance: The class instance of the current object.
        """
        curObjText = self.window.cmb_objType.currentText()
        if curObjText == "Cube":
            return self.cubeObject
        elif curObjText == "Torus":
            return self.torusObject

    def __init__(self, file, parent=None):
        super(ProceduralObjects, self).__init__(parent)
        loader = QtUiTools.QUiLoader()
        mainUIFile = QtCore.QFile(file)
        mainUIFile.open(QtCore.QFile.ReadOnly)
        self.window = loader.load(mainUIFile)
        self.glViewer = None
        mainUIFile.close()

        self.configureWidgets()
        self.loadGLViewer()
        self.cubeObject = cube.ProceduralCube("ui/cubeproceduralwdg.ui", self.glViewer)
        self.torusObject = torus.ProceduralTorus("ui/torusproceduralwdg.ui", self.glViewer)
        self.loadProceduralObject()

    def show(self):
        """Show the main window."""
        self.window.show()

    def configureWidgets(self):
        """Connect signals of all widgets."""
        self.window.cmb_objType.currentIndexChanged.connect(self.loadProceduralObject)
        self.window.act_exit.triggered.connect(QtCore.QCoreApplication.quit)
        self.window.act_restoreDef.triggered.connect(self.restoreObjectDefaults)
        self.window.cbx_shaded.stateChanged.connect(self.retrieveRenderSettings)
        self.window.cbx_smooth.stateChanged.connect(self.retrieveRenderSettings)

    def loadGLViewer(self):
        """Load the GL Widget."""
        self.window.lay_glView = QtWidgets.QVBoxLayout()
        self.window.lay_glView.setContentsMargins(0, 0, 1, 0)
        self.glViewer = OpenGLView()
        self.window.lay_glView.addWidget(self.glViewer)
        self.window.wdg_glView.setLayout(self.window.lay_glView)

    def updateGLViewer(self):
        """Update the GL Widget."""
        self.glViewer.obj = self.findCurrentProceduralObject
        self.glViewer.update()

    def loadProceduralObject(self):
        """Load the procedural object current selected."""
        curObj = self.findCurrentProceduralObjectText
        curLay = self.window.lay_objSettings
        if curLay.count() > 0:
            curLayWidget = curLay.itemAt(0).widget()
            curLay.removeWidget(curLayWidget)
            # curLayWidget.deleteLater()
            curLayWidget.setParent(None)
        if curObj == "Cube":
            curLay.addWidget(self.cubeObject.widget)
        elif curObj == "Torus":
            curLay.addWidget(self.torusObject.widget)
        self.updateGLViewer()

    def restoreObjectDefaults(self):
        """Restores the current object widget to default value."""
        curObj = self.findCurrentProceduralObjectText
        if curObj == "Cube":
            obj = self.cubeObject
        elif curObj == "Torus":
            obj = self.torusObject
        obj.restoreDefaults()

    def retrieveRenderSettings(self):
        """Retrieve a list of all render settings."""
        shaded = self.window.cbx_shaded.isChecked()
        smooth = self.window.cbx_smooth.isChecked()
        settings = [shaded, smooth]
        self.glViewer.render = settings
        self.updateGLViewer()
        return [shaded, smooth]


class OpenGLView(QtWidgets.QOpenGLWidget):
    """Class of the OpenGL View."""

    def __init__(self, obj=None, render=None, parent=None):
        QtWidgets.QOpenGLWidget.__init__(self, parent=parent)
        self.resizeSize = QtCore.QSize(547, 539)
        self._obj = obj
        self._render = render if render is not None else [False, False]
        # Render Settings = [shaded, smooth]

    @property
    def obj(self):
        """Return the current drawing object.

        Returns:
            instace: The instance of the current object.
        """
        return self._obj

    @obj.setter
    def obj(self, newObj):
        """Set the current drawing object."""
        self._obj = newObj

    @property
    def render(self):
        """Return the render settings.

        Returns:
            list: The render settings.
        """
        return self._render

    @render.setter
    def render(self, newSettings):
        """Set the current render settings."""
        self._render = newSettings

    def initializeGL(self):
        """
        This virtual function is called once before the first call to paintGL() or resizeGL(),
        and then once whenever the widget has been assigned a new QGLContext.
        """
        gl.glClearColor(0.14, 0.14, 0.14, 0.0)  # Background color
        gl.glPushAttrib(gl.GL_CURRENT_BIT)
        gl.glDisable(gl.GL_CULL_FACE)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        # gl.glEnable(gl.GL_DEPTH_TEST)
        # gl.glDisable(gl.GL_CULL_FACE)
        # gl.glPushAttrib(gl.GL_CURRENT_BIT)
        # gl.glEnable(gl.GL_BLEND)
        # gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def resizeGL(self, w, h):
        """ This virtual function is called whenever the widget has been resized. """
        # pylint: disable=invalid-name
        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45, (self.resizeSize.width() / self.resizeSize.height()), 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        return None

    def paintGL(self):
        """ This virtual function is called whenever the widget needs to be painted. """
        # gl.glRotatef(self.yRotDeg, self.rotAxis[0], self.rotAxis[1], self.rotAxis[2])
        if self.render[1]:
            gl.glEnable(gl.GL_POINT_SMOOTH)
            gl.glEnable(gl.GL_LINE_SMOOTH)
            gl.glEnable(gl.GL_POLYGON_SMOOTH)
            glfw.init()
            glfw.window_hint(glfw.SAMPLES, 4)
            gl.glEnable(gl.GL_MULTISAMPLE)
            # gl.glHint(gl.GL_MULTISAMPLE_BIT, gl.GL_NICEST)
        else:
            gl.glDisable(gl.GL_POINT_SMOOTH)
            gl.glDisable(gl.GL_LINE_SMOOTH)
            gl.glDisable(gl.GL_POLYGON_SMOOTH)
            gl.glDisable(gl.GL_MULTISAMPLE)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslatef(0.0, 0.0, -5.0)
        gl.glRotatef(15.0, 1.0, 0.0, 0.0)
        self.drawObj()

    def drawObj(self):
        """Draw the current object."""
        try:
            self.obj.draw()
        except AttributeError:
            pass



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = ProceduralObjects("ui/mainproceduralui.ui")
    mainUI.show()
    sys.exit(app.exec_())
