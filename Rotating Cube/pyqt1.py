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
from PySide2 import QtWidgets


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
        self.widget.paint2 = True
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.widget)
        self.setLayout(mainLayout)


class PySideOpenGL(QtWidgets.QOpenGLWidget):
    """ PySide OpenGL Class. """

    def __init__(self, parent=None):
        QtWidgets.QOpenGLWidget.__init__(self, parent=parent)

        self.paint0 = False        # Control what gets painted
        self.paint1 = False
        self.paint2 = False

        self.setMinimumSize(800, 600)

    def initializeGL(self):
        """
        This virtual function is called once before the first call to paintGL() or resizeGL(),
        and then once whenever the widget has been assigned a new QGLContext.
        """
        gl.glClearColor(0.0, 0.0, 1.0, 0.0) # Background color
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    def resizeGL(self, w, h):
        """ This virtual function is called whenever the widget has been resized. """
        # pylint: disable=invalid-name
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-50, 50, -50, 50, -50.0, 50.0)
        gl.glViewport(0, 0, w, h)

    def paintGL(self):
        """ This virtual function is called whenever the widget needs to be painted. """
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
