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
    * PyGame

Todo:
    * NDA

Source:
    * sentdex Youtube channel video: https://www.youtube.com/watch?v=R4n4NyDG2hI
    * https://www.youtube.com/watch?v=R4n4NyDG2hI&list=PLQVvvaa0QuDdfGpqjkEJSeWKGCP31__wD
    * https://www.youtube.com/watch?v=qK9rQaBM5rs
    * https://pythonprogramming.net/community/37/Cube%20rotation%20with%20pyopengl%20and%20pyqt/

This code supports Pylint. Rc file in project.
"""
import pygame
from pygame.locals import *
import OpenGL.GL as gl
import OpenGL.GLU as glu

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


def cube():
    """ Draw a cube. """
    gl.glBegin(gl.GL_LINES)

    for edge in kEdges:
        for vertex in edge:
            gl.glVertex3f(kVerticies[vertex][0], kVerticies[vertex][1], kVerticies[vertex][2]) # or gl.glVertex3fv(kVertices[vertex])

    gl.glEnd()

def main():
    """ Main function. """
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glu.gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    gl.glTranslatef(0.0, 0.0, -5.0)
    gl.glRotatef(0.0, 0.0, 0.0, 0.0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gl.glRotatef(1.0, 3.0, 1.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        cube()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
