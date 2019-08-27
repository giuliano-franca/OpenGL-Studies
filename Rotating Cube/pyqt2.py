# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    MIT License.

How to use:
    * Pass

Requirements:
    * Python 3
    * PyOpenGL
    * PySide2

Todo:
    * NDA

Source:
    * sentdex Youtube channel video: https://www.youtube.com/watch?v=R4n4NyDG2hI
    * https://www.youtube.com/watch?v=R4n4NyDG2hI&list=PLQVvvaa0QuDdfGpqjkEJSeWKGCP31__wD
    * https://www.youtube.com/watch?v=qK9rQaBM5rs | 8:43
    * https://pythonprogramming.net/community/37/Cube%20rotation%20with%20pyopengl%20and%20pyqt/

This code supports Pylint. Rc file in project.
"""
import sys
import OpenGL.GL as gl
from PyQt5 import QtWidgets, QtCore


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

class MainWindow(QtWidgets.QOpenGLWidget):
    """ Main Windows Class. """

    def __init__(self, parent=None):
        QtWidgets.QOpenGLWidget.__init__(self, parent=parent)

        self.widget = PySideOpenGL(self)
        self.widget.paint0 = True
        self.widget.paint1 = True
        # self.widget.paint2 = True
        self.widget.resizeLines = True
        self.widget.paintRotation = True
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.widget)
        self.setLayout(mainLayout)


class PySideOpenGL(QtWidgets.QOpenGLWidget):
    """ PySide OpenGL Class. """
    xRotChanged = QtCore.pyqtSignal(int)
    yRotChanged = QtCore.pyqtSignal(int)
    zRotChanged = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        QtWidgets.QOpenGLWidget.__init__(self, parent=parent)

        self.paint0 = False        # Control what gets painted
        self.paint1 = False
        self.paint2 = False
        self.resizeLines = True     # Set orthographic matrix multiplier to large/small
        self.resizeLines = False

        self.paintRotation = True
        self.paintRotation = False
        self.xRot = 0               # Rotation variables
        self.yRot = 0
        self.zRot = 0

        self.lastPos = QtCore.QPoint()

        self.setMinimumSize(800, 600)

    def initializeGL(self):
        """
        This virtual function is called once before the first call to paintGL() or resizeGL(),
        and then once whenever the widget has been assigned a new QGLContext.
        """
        gl.glClearColor(0.16, 0.16, 0.16, 0.0) # Background color
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDisable(gl.GL_CULL_FACE)
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)

        lightPos = [0, 0, 10, 1.0]
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, lightPos)

    def resizeGL(self, w, h):
        """ This virtual function is called whenever the widget has been resized. """
        # pylint: disable=invalid-name
        side = min(w, h)
        if side < 0:
            return
        gl.glViewport((w - side) // 2, (h - side) // 2, side, side)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        if self.resizeLines:
            gl.glOrtho(-50, 50, -50, 50, -50.0, 50.0)
        else:
            gl.glOrtho(-2, 2, -2, 2, 1.0, 15.0) # original pyramid settings
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self):
        """ This virtual function is called whenever the widget needs to be painted. """
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslatef(0.0, 0.0, -10.0)
        gl.glRotatef(self.xRot / 16.0, 1.0, 0.0, 0.0)
        gl.glRotatef(self.yRot / 16.0, 0.0, 1.0, 0.0)
        gl.glRotatef(self.zRot / 16.0, 0.0, 0.0, 1.0)
        self.draw()

    def draw(self):
        """ Draw objects. """
        if self.paintRotation:
            gl.glColor3f(1.0, 0.0, 0.0)
            gl.glBegin(gl.GL_QUADS)         # Bottom of pyramid
            gl.glNormal3f(0.0, 0.0, -1.0)
            gl.glVertex3f(-1.0, -1.0, 0.0)
            gl.glVertex3f(-1.0, 1.0, 0.0)
            gl.glVertex3f(1.0, 1.0, 0.0)
            gl.glVertex3f(1.0, -1.0, 0.0)
            gl.glEnd()

            gl.glColor3f(0.0, 0.0, 0.0)
            gl.glBegin(gl.GL_TRIANGLES)     # Four sides of pyramid
            gl.glNormal3f(0.0, -1.0, 0.707)
            gl.glVertex3f(-1.0, -1.0, 0.0)
            gl.glVertex3f(1.0, -1.0, 0.0)
            gl.glVertex3f(0.0, 0.0, 1.2)
            gl.glEnd()

            gl.glBegin(gl.GL_TRIANGLES)
            gl.glNormal3f(1.0, 0.0, 0.707)
            gl.glVertex3f(1.0, 1.0, 0.0)
            gl.glVertex3f(-1.0, 1.0, 0.0)
            gl.glVertex3f(0.0, 0.0, 1.2)
            gl.glEnd()

            gl.glBegin(gl.GL_TRIANGLES)
            gl.glNormal3f(0.0, 1.0, 0.707)
            gl.glVertex3f(1.0, 1.0, 0.0)
            gl.glVertex3f(-1.0, 1.0, 0.0)
            gl.glVertex3f(0.0, 0.0, 1.2)
            gl.glEnd()

            gl.glBegin(gl.GL_TRIANGLES)
            gl.glNormal3f(-1.0, 0.0, 0.707)
            gl.glVertex3f(-1.0, 1.0, 0.0)
            gl.glVertex3f(-1.0, -1.0, 0.0)
            gl.glVertex3f(0.0, 0.0, 1.2)
            gl.glEnd()

        if self.paint0:
            gl.glColor3f(1.0, 0.0, 0.0)
            gl.glRectf(-5.0, -5.0, 5.0, 5.0)

        if self.paint1:
            gl.glColor3f(0.0, 1.0, 0.0)
            x = 10
            y = 10
            self.drawLoop(x, y)

        if self.paint2:
            gl.glColor3f(0.0, 0.0, 0.0)
            x = 5
            y = 5
            self.drawLoop(x, y)

    def drawLoop(self, x, y, incr=10):
        """ Loop the drawing info. """
        # pylint: disable=invalid-name
        for _ in range(5):
            self.drawSquareLines(x, y)
            x += incr
            y += incr

    def drawSquareLines(self, x=10, y=10, z=0):
        """ Draw square lines in OpenGL. """
        # pylint: disable=invalid-name
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3f(x, y, z)
        gl.glVertex3f(x, -y, z)

        gl.glVertex3f(x, -y, z)
        gl.glVertex3f(-x, -y, z)

        gl.glVertex3f(-x, -y, z)
        gl.glVertex3f(-x, y, z)

        gl.glVertex3f(-x, y, z)
        gl.glVertex3f(x, y, z)
        gl.glEnd()

    def normalizeAngle(self, angle):
        """ Normalize the rotation angle. """
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def setXRotation(self, angle):
        """ Set x rotation. """
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotChanged.emit(angle)
            self.update()

    def setYRotation(self, angle):
        """ Set y rotation. """
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotChanged.emit(angle)
            self.update()

    def setZRotation(self, angle):
        """ Set z rotation. """
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotChanged.emit(angle)
            self.update()

    def mousePressEvent(self, event):
        """ Mouse Press event handling. """
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        """ Mouse Move event handling. """
        moveX = event.x() - self.lastPos.x()
        moveY = event.y() - self.lastPos.y()
        if event.buttons() & QtCore.Qt.LeftButton:      # Mouse left button
            self.setXRotation(self.xRot + 8 * moveY)
            self.setYRotation(self.yRot + 8 * moveX)

        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self.xRot + 8 * moveY)
            self.setZRotation(self.zRot + 8 * moveX)

        self.lastPos = event.pos()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
