import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import random

SCREEN_SIZE = (800, 600)
SCREEN_COLOR = (0.3, 0.3, 0.3, 1.0)
WINDOW_CREATION_FLAGS = pygame.OPENGL | pygame.DOUBLEBUF
FRAMERATE = 60

VERTEX_SHADER_SOURCE = """
#version 330
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
uniform mat4 projection;

out vec3 Color;
void main() {
    gl_Position = projection * vec4(aPos, 1.0);
    Color = aColor;
}
"""
FRAGMENT_SHADER_SOURCE = """
#version 330
in vec3 Color;
out vec4 FragColor;
void main() {
    FragColor = vec4(Color, 1.0);
}
"""

# INICIALIZAÇÃO PYGAME E CONTEXTO OPENGL
pygame.init()
pygame.display.set_mode(SCREEN_SIZE, WINDOW_CREATION_FLAGS)
clock = pygame.time.Clock()

# COMPILAÇÃO SHADERS
try:
    program = compileProgram(
        compileShader(VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER)
    )
except RuntimeError as e:
    print(f"Erro ao compilar shaders: {e}")
    pygame.quit()
    exit()

left, right = 0, 800
bottom, top = 600, 0
near, far = -1, 1

projection = np.array([
    [2/(right-left), 0, 0, -(right+left)/(right-left)],
    [0, 2/(top-bottom), 0, -(top+bottom)/(top-bottom)],
    [0, 0, -2/(far-near), -(far+near)/(far-near)],
    [0, 0, 0, 1]
], dtype=np.float32)

glUseProgram(program)
proj_loc = glGetUniformLocation(program, "projection")
glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection.T)
glUseProgram(0)

# VAO + VBO
vao = glGenVertexArrays(1)
glBindVertexArray(vao)
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, 0, None, GL_DYNAMIC_DRAW)

# ATRIBUTOS
stride = 6 * 4  # 6 floats (X,Y,Z,R,G,B) * 4 bytes
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * 4))
glEnableVertexAttribArray(1)

glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)

vertices = []

glClearColor(0.0, 0.0, 0.5, 1.0)

# LOOP
running = True
while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # botão esquerdo
                    x, y = event.pos

                    r = random.randint(0, 1)
                    g = random.randint(0, 1)
                    b = random.randint(0, 1)

                    p1 = (x, y-10)
                    p2 = (x-10, y+10)
                    p3 = (x+10, y+10)

                    
                    for (x,y) in (p1, p2, p3):
                        vertices.extend([x, y, 0.0, float(r), float(g), float(b)])

                    
                    data = np.array(vertices, dtype=np.float32)
                    glBindBuffer(GL_ARRAY_BUFFER, vbo)
                    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)
                    glBindBuffer(GL_ARRAY_BUFFER, 0)


        glClearColor(*SCREEN_COLOR)
        glClear(GL_COLOR_BUFFER_BIT)

        if vertices:
            num_vertices = len(vertices) // 6
            glUseProgram(program)
            glBindVertexArray(vao)
            glDrawArrays(GL_TRIANGLES, 0, num_vertices)
            glBindVertexArray(0)
            glUseProgram(0)
        
        pygame.display.flip()
        clock.tick(FRAMERATE)

pygame.quit()