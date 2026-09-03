import pygame
from OpenGL.GL import *

SCREEN_SIZE = (800, 600)
SCREEN_COLOR = (0.3, 0.3, 0.3, 1.0)
WINDOW_CREATION_FLAGS = pygame.OPENGL | pygame.DOUBLEBUF
FRAMERATE = 60

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, WINDOW_CREATION_FLAGS)
clock = pygame.time.Clock()
glClearColor(*SCREEN_COLOR)

modo_poligono = GL_FILL

vertices = [
    (-0.5, 0.5, 0.0),
    (-0.5, -0.5, 0.0),
    (0.0, 0.0, 0.0),
    (0.5, -0.5, 0.0),
    (0.5, 0.5, 0.0)
]

formas = [
    [0, 1, 2],
    [2, 3, 4]
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_1:
                    modo_poligono = GL_FILL
                case pygame.K_2:
                    modo_poligono = GL_LINE
                case pygame.K_3:
                    modo_poligono = GL_POINT

    glClear(GL_COLOR_BUFFER_BIT)
    glPolygonMode(GL_FRONT_AND_BACK, modo_poligono)

    for form in formas:
        glBegin(GL_TRIANGLES)
        glColor3f(0.0, 0.0, 1.0)
        for idx in form:
            glVertex3f(*vertices[idx])
        glEnd()

    glPointSize(3.0)

    pygame.display.flip()
    clock.tick(FRAMERATE)

pygame.quit()