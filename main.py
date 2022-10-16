#!/usr/bin/env python3
import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 800, 800)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def check(num):
    z = 0.0
    n = 0
    while abs(z) <= 2 and n < 50:
        z = z*z + num
        n += 1
    return n


def recursion(x, y, size, steps):   #draws 8 rectangles arround a given one
        if steps == 0: return
        rect(x - size * 2 / 3, y + size * 2 / 3, size / 3)
        rect(x + size * 1 / 3, y + size * 2 / 3, size / 3)
        rect(x + size * 4 / 3, y + size * 2 / 3, size / 3)
        rect(x - size * 2 / 3, y - size * 1 / 3, size / 3)
        rect(x + size * 4 / 3, y - size * 1 / 3, size / 3)
        rect(x - size * 2 / 3, y - size * 4 / 3, size / 3)
        rect(x + size * 1 / 3, y - size * 4 / 3, size / 3)
        rect(x + size * 4 / 3, y - size * 4 / 3, size / 3)
        recursion(x - size * 2 / 3, y + size * 2 / 3, size / 3, steps - 1)
        recursion(x + size * 1 / 3, y + size * 2 / 3, size / 3, steps - 1)
        recursion(x + size * 4 / 3, y + size * 2 / 3, size / 3, steps - 1)
        recursion(x - size * 2 / 3, y - size * 1 / 3, size / 3, steps - 1)
        recursion(x + size * 4 / 3, y - size * 1 / 3, size / 3, steps - 1)
        recursion(x - size * 2 / 3, y - size * 4 / 3, size / 3, steps - 1)
        recursion(x + size * 1 / 3, y - size * 4 / 3, size / 3, steps - 1)
        recursion(x + size * 4 / 3, y - size * 4 / 3, size / 3, steps - 1)


def rect(x, y, size): #draws a rectangle given top left corner and size
    glColor3ub(230, 230, 230)
    glBegin(GL_TRIANGLE_STRIP)
    glVertex2f(x,y)
    glVertex2f(x+size,y)
    glVertex2f(x,y-size)
    glVertex2f(x+size,y-size)
    glEnd()


def render(time,no_steps,program):
    if program == 1:
        size_min = -800                         #size of the frame
        size_max = 800
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3ub(144, 128, 0)                 #color of the background
    
        glBegin(GL_TRIANGLE_STRIP)              #generating background
        glVertex2f(size_min, size_min)
        glVertex2f(size_max, size_min)
        glVertex2f(size_min, size_max)
        glVertex2f(size_max,size_max)
        glEnd()
        rect(-800/3, 800/3,800*2/3)             #first rectangle
        recursion(-800 / 3, 800 / 3, 800 * 2 / 3, no_steps)
        glFlush()
    if program == 2:
        real_start = -2
        real_end = 1
        im_start = -1
        im_end = 1
        _range = 800
        for row in range(_range):
            for column in range(_range):
                c = complex(real_start + (row / 800) * (real_end - real_start),
                            im_start + (column / 800) * (im_end - im_start))
                data = check(c)
                glBegin(GL_POINTS)
                glColor3ub(255 - int(data * 255 / 50), 400 - int(data * 400 / 50), 0)
                glVertex2f(2 * row - 800, 2 * column - 800)
                glEnd()
        glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-800.0, 800.0, -800.0 / aspect_ratio, 800.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-800.0 * aspect_ratio, 800.0 * aspect_ratio, -800.0, 800.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    print("Which program do you want to open:\n1. Sierpinski Carpet\n2. Mandelbrot Set")
    program = int(input())
    steps=0
    if program==1:
        print("How many steps of recursion do you want? \nMore than 7 may be too much ;) \nNumber of steps:")
        steps = int(input())

    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(800, 800, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):

        render(glfwGetTime(),steps,program)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()

