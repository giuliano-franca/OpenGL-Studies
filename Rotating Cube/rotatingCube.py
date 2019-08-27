# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    MIT License.

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

How to use:
    * Install Python 3. (I'm using Python 3.7.4)
    * Pip install all the dependencies.
    * Run the file.

Dependencies:
    * Python 3
    * PyOpenGL
    * PySide2

Todo:
    * Add the other draw types
    * Fix the rotation intensity to all fps settings.
    * Add wireframe drawing option.
    * [FUTURE] Add a import file based system to read FBX in a future version.

Sources:
    * sentdex Youtube channel video: https://www.youtube.com/watch?v=R4n4NyDG2hI
    * https://www.youtube.com/watch?v=R4n4NyDG2hI&list=PLQVvvaa0QuDdfGpqjkEJSeWKGCP31__wD
    * https://www.youtube.com/watch?v=qK9rQaBM5rs
    * https://pythonprogramming.net/community/37/Cube%20rotation%20with%20pyopengl%20and%20pyqt/
    * https://codeloop.org/python-modern-opengl-rotating-the-cube/

This code supports Pylint. Rc file in project.
"""
import sys
import OpenGL.GL as gl
import OpenGL.GLU as glu
from PySide2 import QtWidgets, QtCore


kVerticies = [[1.0, -1.0, -1.0],
              [1.0, 1.0, -1.0],
              [-1.0, 1.0, -1.0],
              [-1.0, -1.0, -1.0],
              [1.0, -1.0, 1.0],
              [1.0, 1.0, 1.0],
              [-1.0, -1.0, 1.0],
              [-1.0, 1.0, 1.0]]

kEdges = [[0, 1],
          [0, 3],
          [0, 4],
          [2, 1],
          [2, 3],
          [2, 7],
          [6, 3],
          [6, 4],
          [6, 7],
          [5, 1],
          [5, 4],
          [5, 7]]

kSurfaces = [[0, 1, 2, 3],
             [3, 2, 7, 6],
             [6, 7, 5, 4],
             [4, 5, 1, 0],
             [1, 5, 7, 2],
             [4, 0, 3, 6]]


class DrawTypes(object):
    """
    Types of drawing.\n
    Enum {
        kCubeLines
        kCube
        kPyramidLines
        kPyramid
    }
    """
    kCubeLines = 0
    kCube = 1
    kPyramidLines = 2
    kPyramid = 3


class MainWindow(QtWidgets.QMainWindow):
    """ Main Windows Class. """

    def __init__(self, parent=None):
        # pylint: disable=unnecessary-lambda, no-member
        QtWidgets.QMainWindow.__init__(self, parent=parent)

        self.widget = PySideOpenGL(self)
        self.setCentralWidget(self.widget)

        self.widget.drawType = DrawTypes.kCube
        self.widget.rotMult = 1.0

        self.fpsList = {"12": 1000.0 / 12.0,
                        "24": 1000.0 / 24.0,
                        "29.97": 1000.0 / 29.97,
                        "30": 1000.0 / 30.0,
                        "60": 1000.0 / 60.0}

        self.exitAction = QtWidgets.QAction('Quit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip("Exit application.")
        self.exitAction.triggered.connect(lambda: QtCore.QCoreApplication.quit())
        self.drawCubeLinesAction = QtWidgets.QAction('Cube wireframe', self)
        self.drawCubeLinesAction.triggered.connect(lambda: self.setDrawType(DrawTypes.kCubeLines))
        self.drawCubeAction = QtWidgets.QAction('Cube', self)
        self.drawCubeAction.triggered.connect(lambda: self.setDrawType(DrawTypes.kCube))
        self.drawPyramidLinesAction = QtWidgets.QAction('Pyramid wireframe', self)
        # self.drawPyramidLinesAction.triggered.connect()
        self.drawPyramidAction = QtWidgets.QAction('Pyramid', self)
        # self.drawPyramidAction.triggered.connect()
        self.playAnimationAction = QtWidgets.QAction('Toggle animation', self)
        self.playAnimationAction.setCheckable(True)
        self.playAnimationAction.setChecked(False)
        self.playAnimationAction.setShortcut('K')
        self.playAnimationAction.toggled.connect(self.togglePlayAnimation)
        self.fpsActionList = []
        self.setFPS12Action = QtWidgets.QAction('12 FPS', self)
        self.setFPS12Action.triggered.connect(lambda: self.setFPS("12"))
        self.setFPS12Action.setCheckable(True)
        self.fpsActionList.append(self.setFPS12Action)
        self.setFPS24Action = QtWidgets.QAction('24 FPS', self)
        self.setFPS24Action.triggered.connect(lambda: self.setFPS("24"))
        self.setFPS24Action.setCheckable(True)
        self.fpsActionList.append(self.setFPS24Action)
        self.setFPS2997Action = QtWidgets.QAction('29.97 FPS', self)
        self.setFPS2997Action.triggered.connect(lambda: self.setFPS("29.97"))
        self.setFPS2997Action.setCheckable(True)
        self.fpsActionList.append(self.setFPS2997Action)
        self.setFPS30Action = QtWidgets.QAction('30 FPS', self)
        self.setFPS30Action.triggered.connect(lambda: self.setFPS("30"))
        self.setFPS30Action.setCheckable(True)
        self.fpsActionList.append(self.setFPS30Action)
        self.setFPS60Action = QtWidgets.QAction('60 FPS', self)
        self.setFPS60Action.triggered.connect(lambda: self.setFPS("60"))
        self.setFPS60Action.setCheckable(True)
        self.fpsActionList.append(self.setFPS60Action)

        fileMenu = self.menuBar().addMenu("&File")
        drawTypeMenu = fileMenu.addMenu("&Draw Type")
        drawTypeMenu.addAction(self.drawCubeLinesAction)
        drawTypeMenu.addAction(self.drawCubeAction)
        drawTypeMenu.addAction(self.drawPyramidLinesAction)
        drawTypeMenu.addAction(self.drawPyramidAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)
        animationMenu = self.menuBar().addMenu("&Animation")
        animationMenu.addAction(self.playAnimationAction)
        self.fpsMenu = animationMenu.addMenu("&Set FPS")
        self.fpsMenu.addAction(self.setFPS12Action)
        self.fpsMenu.addAction(self.setFPS24Action)
        self.fpsMenu.addAction(self.setFPS2997Action)
        self.fpsMenu.addAction(self.setFPS30Action)
        self.fpsMenu.addAction(self.setFPS60Action)

        self.timer = QtCore.QTimer(self)
        self.setFPS("24")
        self.timer.timeout.connect(self.widget.spin)

        self.setWindowTitle("Testing PyOpenGL with PySide2")

    def togglePlayAnimation(self):
        """ Toggle play animation. """
        if self.playAnimationAction.isChecked():
            self.timer.start()
        else:
            self.timer.stop()

    def setFPS(self, fps):
        """ Set the Frame per Second. """
        self.timer.setInterval(self.fpsList[fps])
        for action in self.fpsActionList:
            if fps in action.text():
                action.setChecked(True)
            else:
                action.setChecked(False)

    def setDrawType(self, typ):
        """ Set the draw type geometry. """
        self.widget.drawType = typ
        self.widget.update()


class PySideOpenGL(QtWidgets.QOpenGLWidget):
    """ PySide OpenGL Class. """

    def __init__(self, parent=None):
        QtWidgets.QOpenGLWidget.__init__(self, parent=parent)

        self.yRotDeg = 0.0
        self.rotMult = 1.0
        self.rotAxis = [1.0, 1.0, 1.0]
        self.resizeSize = QtCore.QSize(800, 600)
        self.drawType = DrawTypes.kCubeLines

        self.setMinimumSize(self.resizeSize)

    def initializeGL(self):
        """
        This virtual function is called once before the first call to paintGL() or resizeGL(),
        and then once whenever the widget has been assigned a new QGLContext.
        """
        gl.glClearColor(0.16, 0.16, 0.16, 0.0)  # Background color
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDisable(gl.GL_CULL_FACE)
        gl.glPushAttrib(gl.GL_CURRENT_BIT)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def resizeGL(self, w, h):
        """ This virtual function is called whenever the widget has been resized. """
        # pylint: disable=invalid-name
        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45, (self.resizeSize.width() / self.resizeSize.height()), 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self):
        """ This virtual function is called whenever the widget needs to be painted. """
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslatef(0.0, 0.0, -5.0)
        gl.glRotatef(self.yRotDeg, self.rotAxis[0], self.rotAxis[1], self.rotAxis[2])
        self.draw()

    def draw(self):
        """ Draw objects. """
        if self.drawType == DrawTypes.kCubeLines:
            gl.glBegin(gl.GL_LINES)
            for edge in kEdges:
                for vertex in edge:
                    if vertex % 2 == 0:
                        gl.glColor3f(1.0, 0.0, 0.0)
                    else:
                        gl.glColor3f(0.0, 1.0, 1.0)
                    gl.glVertex3f(kVerticies[vertex][0], kVerticies[vertex][1], kVerticies[vertex][2])  # or gl.glVertex3fv(kVertices[vertex])
            gl.glEnd()
        elif self.drawType == DrawTypes.kCube:
            gl.glBegin(gl.GL_QUADS)
            for surface in kSurfaces:
                gl.glColor4f(0.5, 0.5, 0.5, 1.0)
                for vertex in surface:
                    gl.glVertex3f(kVerticies[vertex][0], kVerticies[vertex][1], kVerticies[vertex][2])
            # gl.glColor4f(0.6, 0.6, 0.6, 0.6)
            # for i in range(len(kVerticies) - 1):
            #     gl.glVertex3f(kVerticies[i][0], kVerticies[i][0], kVerticies[i][0])
            gl.glEnd()
            gl.glBegin(gl.GL_LINES)
            gl.glColor3f(1.0, 1.0, 1.0)
            # for i in range(len(kVerticies) - 1):
            #     gl.glVertex3f(kVerticies[i][0], kVerticies[i][1], kVerticies[i][2])
            #     gl.glVertex3f(kVerticies[i + 1][0], kVerticies[i + 1][1], kVerticies[i + 1][2])
            for edge in kEdges:
                for vertex in edge:
                    gl.glVertex3f(kVerticies[vertex][0], kVerticies[vertex][1], kVerticies[vertex][2])  # or gl.glVertex3fv(kVertices[vertex])
            gl.glEnd()
        else:
            pass

    def spin(self):
        """ Spin the cube. """
        self.yRotDeg = (self.yRotDeg + self.rotMult) % 360.0
        self.update()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
