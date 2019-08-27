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
    * Numpy

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
import math
import collections
import numpy as np
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
        kTorus
        kPyramidLines
        kPyramid
    }
    """
    kCubeLines = 0
    kCube = 1
    kTorus = 2


class MainWindow(QtWidgets.QMainWindow):
    """ Main Windows Class. """

    def __init__(self, parent=None):
        # pylint: disable=unnecessary-lambda, no-member
        QtWidgets.QMainWindow.__init__(self, parent=parent)

        self.widget = PySideOpenGL(self)
        self.setCentralWidget(self.widget)

        self.widget.drawType = DrawTypes.kTorus
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
        self.drawTorusLinesAction = QtWidgets.QAction('Torus wireframe', self)
        self.drawTorusLinesAction.triggered.connect(lambda: self.setDrawType(DrawTypes.kTorus))
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
        drawTypeMenu.addAction(self.drawTorusLinesAction)
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
        self.setFPS("60")
        self.timer.timeout.connect(self.widget.spin)

        self.setWindowTitle("Testing PyOpenGL with PySide2 - Procedural objects")

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
            gl.glColor3f(1.0, 1.0, 1.0)
            for edge in kEdges:
                for vertex in edge:
                    gl.glVertex3f(kVerticies[vertex][0], kVerticies[vertex][1], kVerticies[vertex][2])  # or gl.glVertex3fv(kVertices[vertex])
            gl.glEnd()
            # width = 1.0         # X
            # height = 1.0        # Y
            # depth = 1.0         # Z
            # subdWidth = 1
            # subdHeight = 1
            # subdDepth = 1
            # gl.glPointSize(3)
            # gl.glBegin(gl.GL_POINTS)
            # for w in range(subdWidth):
            #     wStep = width / subdWidth
            #     for h in range(subdHeight):
            #         hStep = height / subdHeight
            #         gl.glVertex3f(wStep * (w - width), hStep * (w - height), 0.0)
            # gl.glEnd()
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
        elif self.drawType == DrawTypes.kTorus:
            subdAxis = 15
            subdHeight = 20
            radius = 1.0
            radiusSec = 0.5
            step = 2.0 * math.pi / subdAxis
            stepSec = 2.0 * math.pi / subdHeight
            loops = collections.OrderedDict()
            for i in range(subdAxis):
                gl.glColor3f(1.0, 0.0, 0.0)
                alpha = step * i + (math.pi / 2.0)
                mOrigin = np.identity(4)
                mOrigin[0][0] = math.cos(-alpha)
                mOrigin[0][2] = -math.sin(-alpha)
                mOrigin[2][0] = math.sin(-alpha)
                mOrigin[2][2] = math.cos(-alpha)
                mOrigin[3][0] = math.cos(step * i) * radius
                mOrigin[3][2] = math.sin(step * i) * radius
                pivotInfo = collections.OrderedDict()
                for j in range(subdHeight):
                    gl.glColor3f(1.0, 1.0, 1.0)
                    beta = stepSec * j
                    mChildL = np.identity(4)
                    mChildL[3][1] = -math.sin(beta) * radiusSec
                    mChildL[3][2] = math.cos(beta) * radiusSec
                    mChildW = np.matmul(mChildL, mOrigin)
                    pivotInfo["Point %s" % j] = [mChildW[3][0], mChildW[3][1], mChildW[3][2]]
                loops["Pivot %s" % i] = pivotInfo
            gl.glBegin(gl.GL_LINES)
            for i in range(subdAxis):
                for j in range(subdHeight):
                    gl.glColor3f(1.0, 1.0, 1.0)
                    aID = i + 1
                    if aID == subdAxis:
                        aID = 0
                    pID = j + 1
                    if pID == subdHeight:
                        pID = 0
                    startAxis = loops["Pivot %s" % str(i)]["Point %s" % str(j)]
                    endAxis = loops["Pivot %s" % str(aID)]["Point %s" % str(j)]
                    startHeight = loops["Pivot %s" % str(i)]["Point %s" % str(j)]
                    endHeight = loops["Pivot %s" % str(i)]["Point %s" % str(pID)]
                    gl.glVertex3f(startAxis[0], startAxis[1], startAxis[2])
                    gl.glVertex3f(endAxis[0], endAxis[1], endAxis[2])
                    gl.glColor3f(1.0, 1.0, 1.0)
                    gl.glVertex3f(startHeight[0], startHeight[1], startHeight[2])
                    gl.glVertex3f(endHeight[0], endHeight[1], endHeight[2])
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
