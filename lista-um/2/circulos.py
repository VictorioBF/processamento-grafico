import pygame, math
from OpenGL.GL import *

SCREEN_SIZE = (600, 600)
SCREEN_COLOR = (0.3, 0.3, 0.3, 1.0)
WINDOW_CREATION_FLAGS = pygame.OPENGL | pygame.DOUBLEBUF
FRAMERATE = 10

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, WINDOW_CREATION_FLAGS)
clock = pygame.time.Clock()
glClearColor(*SCREEN_COLOR)

modo_poligono = GL_FILL

step = 0.0
mode = GL_TRIANGLE_FAN
num_segments = 50
qtt_loops = 1
max_angle = 360
min_angle = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_1:
                    qtt_loops = 1
                    mode = GL_TRIANGLE_FAN
                    num_segments = 8
                    step = 0
                    max_angle = 360
                    min_angle = 0
                    glColor3f(1.0, 1.0, 1.0)
                case pygame.K_2:
                    qtt_loops = 1
                    mode = GL_TRIANGLE_FAN
                    num_segments = 5
                    step = 0
                    max_angle = 360
                    min_angle = 0
                    glColor3f(1.0, 1.0, 1.0)
                case pygame.K_3:
                    qtt_loops = 1
                    mode = GL_TRIANGLE_FAN
                    num_segments = 50
                    step = 0
                    max_angle = 330
                    min_angle = 30
                    glColor3f(1.0, 1.0, 0.0)
                case pygame.K_4:
                    qtt_loops = 1
                    mode = GL_TRIANGLE_FAN
                    num_segments = 50
                    step = 0
                    max_angle = 300
                    min_angle = 240
                    glColor3f(1.0, 1.0, 0.0)
                case pygame.K_5:
                    qtt_loops = 4
                    mode = GL_LINE_STRIP
                    num_segments = 50
                    step = 0.0025
                    max_angle = 360
                    min_angle = 0
                    glColor3f(1.0, 1.0, 1.0)

    glClear(GL_COLOR_BUFFER_BIT)
    glPolygonMode(GL_FRONT_AND_BACK, modo_poligono)

    x = y = 0
    radius = 0.5

    glLineWidth(3.0)
    glBegin(mode)
    if mode == GL_TRIANGLE_FAN:
        glVertex2f(x, y)
    for _ in range(qtt_loops):
        for i in range(num_segments + 1):
            theta = 2.0 * math.pi * float(i) / float(num_segments)
            if theta > (max_angle/180*math.pi) or theta < (min_angle/180*math.pi):
                continue
            dx = radius * math.cos(theta)
            dy = radius * math.sin(theta)
            radius = radius - step
            glVertex2f(x + dx, y + dy)
    glEnd()

    glPointSize(3.0)

    pygame.display.flip()
    clock.tick(FRAMERATE)

pygame.quit()