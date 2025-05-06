from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random




def draw_points(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x,y) 
    glEnd()

def find_zone(x0,x1,y0,y1):
    dx = x1-x0
    dy = y1-y0

    zone = -1

    if abs(dx)>abs(dy):
        if dx>=0 and dy>=0:
            zone = 0
        elif dx<0  and dy>=0:
            zone = 3
        elif dx<0  and dy<0:
            zone = 4
        elif dx>=0  and dy<0:
            zone = 7
        
    else:
        if dx>=0 and dy>=0:
            zone = 1
        elif dx<0  and dy>=0:
            zone = 2
        elif dx<0  and dy<0:
            zone = 5
        elif dx>=0  and dy<0:
            zone = 6

    return zone
def convert_zone_zero(zone,x,y):
    if zone == 0:
        return x,y
    elif zone == 1:
        return y,x
    elif zone == 2:
        return y,-x
    elif zone == 3:
        return -x,y
    elif zone == 4:
        return -x,-y
    elif zone == 5:
        return -y,-x
    elif zone == 6:
        return -y,x
    elif zone == 7:
        return x,-y

def convert_original(zone,x,y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y
    
def midpoint_algo(startx,starty,endx,endy,zone):
    dx = endx-startx
    dy = endy-starty

    d = (2*dy)-dx
    x = startx
    y = starty

    while x<=endx:
        org_x,org_y = convert_original(zone,x,y)
        draw_points(org_x,org_y)

        if d>0: #NE
            x+=1
            y+=1
            d+= (2*(dy-dx))
        elif d<=0:
            x+=1
            d+= (2*dy)




def eightway(x0,x1,y0,y1):
    zone = find_zone(x0,x1,y0,y1)
    startx,starty = convert_zone_zero(zone,x0,y0)
    endx,endy = convert_zone_zero(zone,x1,y1)
    midpoint_algo(startx,starty,endx,endy,zone)
    
def midpoint_circle(x,y,r):


    d = 1-r
    x_p = 0
    y_p = r

    while x_p<=y_p:
        glColor3f(1,1.0,0)
        draw_points(x_p+x, y_p+y)
        draw_points(-x_p+x, y_p+y)
        draw_points(-y_p+x, x_p+y)
        draw_points(-y_p+x, -x_p+y)
        draw_points(-x_p+x, -y_p+y)
        draw_points(x_p+x, -y_p+y)
        draw_points(y_p+x, -x_p+y)
        draw_points(y_p+x, x_p+y)


        if d>0: 
            x_p+=1
            y_p-=1
            d = d + (2 * (x_p - y_p)) + 5
        elif d<=0:
            x_p+=1
            d = d + (2 * x_p) + 3





def cross_func() :

    glColor3f(1.0,0.0,0.0)
    eightway(460,480,697,665)
    eightway(460,480,665,697)

def pause():
    
    glColor3f(1,1.0,0)
    eightway(250,250,697,660)
    eightway(275,275,660,697)

def back():
    
    glColor3f(0,1,1)
    eightway(30,60,675,675)
    eightway(30,40,675,695)
    eightway(30,40,675,655)
def play():
    glColor3f(1,1.0,0)
    eightway(275,250,697,675)
    eightway(275,275,660,697)
    eightway(275,250,660,675)


bubbles = []

game = False
shooter_r = 15
shooterx = 250
shootery = 30

def is_overlapping(new_x, new_y, new_r):
    for (x, y, r) in bubbles:
        distance = math.sqrt((new_x - x)**2 + (new_y - y)**2)
        if distance < new_r + r: 
            return True
    return False


def bubble():
    global bubbles, hit
    if not game and not paused:
        for i in range(len(bubbles)):
            x, y, r = bubbles[i]
            y -= 0.2  
            bubbles[i] = (x, y, r)


        if len(bubbles)<5:
        
        
            new_x = random.randrange(40,460)
            new_y = random.randrange(520,660)
            new_r = random.randrange(15,30)

        

            if not is_overlapping(new_x, new_y, new_r):
                bubbles.append((new_x, new_y, new_r))

def draw_bubbles():
    for (x, y, r) in bubbles:
        midpoint_circle(x, y, r)


def shooter():
    global shooter_r,shooterx, shootery, game 
    if game:
        glColor3f(1.0, 0.0, 0.0)  
    else:
        glColor3f(1, 1, 0)
        midpoint_circle(shooterx,shootery,shooter_r)

def move_shooter(direction):
    global bulletx , shooterx,shootery,shooter_r
    if direction == 'right' and shooterx+shooter_r<480:
        shooterx+=20
        bulletx = shooterx
        
    elif direction == 'left' and shooterx-shooter_r>20:
        shooterx-=20
        bulletx = shooterx

hit = False
bulletr = 3
bulletx = shooterx
bullety = shootery
score = 0





def draw_bullet():
    global bulletx, bullety, bulletr
    midpoint_circle(bulletx, bullety, bulletr)

def shoot():
    global shooterx, shootery, bulletx, bullety, bulletr,bullet,hit,bulletcount
    if not game and not paused:
        if not hit:
            bullety+=5

            if bulletr+bullety > 700:
                bullet = False
                bulletx = shooterx
                bullety = shootery
                bulletcount+=1
        else:
            bullet = False
            bulletx = shooterx
            bullety = shootery
            hit = False
            


circlecount = 0 
bulletcount = 0

def collison():
    global bulletx, bullety, bulletr, hit,score,game, paused
    if not game and not paused:
        for i, (x, y, r) in enumerate(bubbles):

            distance = math.sqrt((x-bulletx)**2 + (y-bullety)**2)
            if distance < bulletr+ r: 
                hit = True
                score += 1 
                print(f"Score: {score}")
                bubbles.pop(i) 
                break

def update():
    global game,score,paused,shooterx,shootery, bullety,bulletr, circlecount, bulletcount,cross
    
    if not game and not paused:
        for i,  (x, y, r) in enumerate(bubbles):
            distance = math.sqrt((x - shooterx)**2 + (y - shootery)**2)
            if distance < shooter_r + r:  
                game = True
                print(f"Game Over. Final Score: {score}") 
                break
            if y - r < 0:
                circlecount+= 1  
                print(f"Missed circles: {circlecount}")  
                bubbles.pop(i)
            
            if circlecount == 3 or bulletcount == 3:
                game = True
                bulletcount == 0
                circlecount == 0
                print(f"Game Over. Final Score: {score}") 
                break

    if cross:
        game = True
        print(f"Goodbye. Final Score: {score}")

        
def restart_game():
    print("Starting over")
    global bubbles, game, paused, shooterx, shootery, shooter_r, bulletx, bullety, bulletr, bullet, score, circlecount,bulletcount, cross

    bubbles = []
    game = False
    paused = False
    bulletcount = 0
    circlecount = 0
    score = 0
    cross = False

    shooterx = 250
    shootery = 30
    shooter_r = 15

    bulletx = shooterx
    bullety = shootery
    bulletr = 3
    bullet = False

paused = False

def iterate():
    glViewport(0, 0, 500, 750)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 750, -1.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

cross = False

def mouse(button, state, x, y):
    global cross,paused
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        if 30<=x<=60 and 55<=y<=75:
            restart_game()
        elif 460<=x<=480 and 53<=y<=85:
            cross = True
        elif 250<=x<=275 and 50<=y<=85:
            paused = not paused
            
    glutPostRedisplay()

bullet = False

def keyboard(key, x, y):

    global bullet
    if not game and not paused:

        if key == b"a":
            move_shooter('left')
            
        elif key == b"d":
            move_shooter('right')
        if key == b' ':
            if bullet == False:
                bullet= True
                print("Shot")


def showScreen():
    global bullet
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    
    cross_func()
    if not paused:

        pause()
        
    else:
        play()

    back()
    shooter()
    draw_bubbles()

    if not game:
        update()
    if bullet:
        draw_bullet()
        shoot()
        collison()

    bubble()
        
    if (cross == True) :
        glutLeaveMainLoop()

    glFlush()
    glutSwapBuffers()




glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 750) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Shoot The Circles!") #window name
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutIdleFunc(showScreen)

glutMainLoop()