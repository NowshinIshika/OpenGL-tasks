from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random 
import time 
W_Width, W_Height = 500,500

speed = 0.02
ball_size = 5
points = []
animation = True
blink = False
class point:
    def __init__(self,x,y,c1,c2,color):
        self.x=x
        self.y=y
        self.c1 = c1
        self.c2 = c2
        self.color = color 


def crossProduct(a, b):
    result=point()
    result.x = a.y * b.z - a.z * b.y
    result.y = a.z * b.x - a.x * b.z
    result.z = a.x * b.y - a.y * b.x

    return result

def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y 
    return a,b

def draw_points():
    global points

    for p in points:
        if blink:
            glColor3f(0,0,0)
        else:
            glColor3f(*p.color)
        glPointSize(ball_size)
        glBegin(GL_POINTS)
        glVertex2f(p.x, p.y)
        glEnd()

    

def keyboardListener(key, x, y):

    global animation
    if key==b' ':
        animation = not animation
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global speed
    if animation:
        if key==GLUT_KEY_UP:
            speed *= 2
            print("Speed Increased")
        if key== GLUT_KEY_DOWN:		#// up arrow key
            speed /= 2
            print("Speed Decreased")
    glutPostRedisplay()


def mouseListener(button, state, x, y):	#/#/x, y is the x-y of the screen (2D)
    global points,blink
    if animation:
        if button==GLUT_LEFT_BUTTON:
            if(state == GLUT_DOWN):   
                blink = not blink
            
            if (state == GLUT_UP):
                blink = not blink


        if button==GLUT_RIGHT_BUTTON:
            if state == GLUT_DOWN: 	
                c_x, c_y = convert_coordinate(x,y)
                print(x,y)
                c1,c2 = random.choice([(-1, 1), (-1, -1), (1,1), (1, -1)])
                color = (random.random(),random.random(),random.random())
                points.append(point(c_x,c_y,c1,c2,color))





    glutPostRedisplay()


def display():
    #//clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0);	#//color black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)

    draw_points()
    glutSwapBuffers()


def animate():
    global points, speed
    if animation:
        for p in points:
            p.x += p.c1 * speed
            p.y += p.c2 * speed
            if p.x > W_Width / 2 or p.x < -W_Width / 2:
                p.c1 *= -1
            if p.y > W_Height / 2 or p.y < -W_Height / 2:
                p.c2 *= -1
    glutPostRedisplay()

def init():
    #//clear the screen
    glClearColor(0,0,0,0)
    #//load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    #//initialize the matrix
    glLoadIdentity()
    #//give PERSPECTIVE parameters
    gluPerspective(104,	1,	1,	1000.0)
    # **(important)**aspect ratio that determines the field of view in the X direction (horizontally). The bigger this angle is, the more you can see of the world - but at the same time, the objects you can see will become smaller.
    #//near distance
    #//far distance


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color

# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"Blinking Lights")
init()

glutDisplayFunc(display)	#display callback function
glutIdleFunc(animate)	#what you want to do in the idle time (when no drawing is occuring)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()		