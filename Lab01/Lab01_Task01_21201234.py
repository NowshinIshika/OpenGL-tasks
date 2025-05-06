from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

raindrops=[]
bend = 0
s= 1
g = 1
h = 0.7
r = 1
def draw_lines(x1, y1,x2,y2):
    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3f(0, 0, 0)
    glVertex2f(x1, y1)  
    glVertex2f(x2, y2) 
    
 
    glEnd()
def draw_triangle_night(): 
    global h   
    glBegin(GL_TRIANGLES)
    glColor3f(h,h,h)
    glVertex2d(-100,0)
    glVertex2d(100,0)
    glVertex2d(0,75)
    glEnd()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -250, 250, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw_gradient_background_night():
    global s
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, s) 
    glVertex2f(-250, 250)
    glVertex2f(250, 250)
    glColor3f(1,1,1)
    glVertex2f(250, -230)
    glVertex2f(-250, -230)
    glEnd()

def night_grass():
    global g
    glBegin(GL_QUADS)
    glColor3f(0.0, g, 0.0)  # Lighter green color
    glVertex2f(-250, -100)
    glVertex2f(250, -100)
    glVertex2f(250, -250)
    glVertex2f(-250, -250)
    glEnd()
    


def raindrop_night():
    global raindrops
    raindrops.append([random.randrange(-249,250),random.randrange(-249,250),random.randint(20,30),0])
def draw_raindrop(x, y, length):
    global bend, r


    glColor3f(r,r, r)  
    glBegin(GL_LINES)
    glVertex2f(x, y) 
    glVertex2f(x+bend, y - length)

    glEnd()
def draw_night():
    global raindrops
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 1.0) #konokichur color set (RGB)
    #call the draw methods here
    
    draw_gradient_background_night()
    night_grass()
    draw_triangle_night()


    draw_lines(-90,0,-90,-100)
    draw_lines(90,0,90,-100)
    draw_lines(-90,-100,90,-100)

    draw_lines(-45,-100,-45,-30)
    draw_lines(-5,-100,-5,-30)
    draw_lines(-45,-30,-5,-30)

    global raindrops
    global bend

    rain_speed=0.75
    if len(raindrops) < 200:  # Limit the number of raindrops
        raindrop_night()

    for raindrop in raindrops:
        raindrop[0] += bend* 0.01
        raindrop[1] -= rain_speed 
        if raindrop[1] < -250: 
            raindrops.remove(raindrop)
        else:
            draw_raindrop(raindrop[0], raindrop[1], raindrop[2])
    glutSwapBuffers()

def specialKeyListener(key, x, y):
    global raindrops
    global bend
    global s,g,h,r
    if key==GLUT_KEY_RIGHT:
        for raindrop in raindrops:
            bend+=0.1
 
        
        print("right")
    elif key==GLUT_KEY_LEFT:
        for raindrop in raindrops:
            bend-=0.1

    if key == GLUT_KEY_UP:
        if h<0.7:
            s +=0.2
            g += 0.2
            r -=0.1
            
            h +=0.1
        
            print("day")

    elif key == GLUT_KEY_DOWN:
        if s>0.3 and g>0.3:
            s -=0.2
            g -= 0.2
            r +=0.1
            h -=0.1
            print("night")

        

    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) #window size
glutInitWindowPosition(0,0)
wind = glutCreateWindow(b"Raindrops") #window name
glClearColor(0.0, 0.0, 0, 1.0)
glutDisplayFunc(draw_night)
glutIdleFunc(draw_night)
glutSpecialFunc(specialKeyListener)
glutMainLoop()
