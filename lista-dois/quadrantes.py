import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

left, right = 0, 800
bottom, top = 600, 0
near, far = -1, 1

projection = np.array([
    [2/(right-left), 0, 0, -(right+left)/(right-left)],
    [0, 2/(top-bottom), 0, -(top+bottom)/(top-bottom)],
    [0, 0, -2/(far-near), -(far+near)/(far-near)],
    [0, 0, 0, 1]
], dtype=np.float32)

SCREEN_SIZE = (800, 600)
SCREEN_COLOR = (0.3, 0.3, 0.3, 1.0)
WINDOW_CREATION_FLAGS = pygame.OPENGL | pygame.DOUBLEBUF
FRAMERATE = 60

# SHADERS
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
in vec3 Color;                        // Recebe a cor do Vertex Shader
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
    shader_program = compileProgram(
        compileShader(VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER)
    )
except RuntimeError as e:
    print(f"Erro ao compilar shaders: {e}")
    pygame.quit()
    exit()

# DEFINIÇÃO TRIÂNGULO
dados_vertices = np.array([
    400.0, 100.0, 0.0, 1.0, 0.0, 1.0,
    200.0, 500.0, 0.0, 1.0, 0.0, 1.0,
    600.0, 500.0, 0.0, 1.0, 0.0, 1.0
], dtype=np.float32)


# CRIAÇÃO VAO
vao = glGenVertexArrays(1)
glBindVertexArray(vao)

# CRIAÇÃO VBO
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, dados_vertices.nbytes, dados_vertices, GL_STATIC_DRAW)

# CONFIGURAÇÃO ATRIBUTOS
# Posição
posicao_stride = 6 * 4  # 6 floats (X,Y,Z,R,G,B) * 4 bytes
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, posicao_stride, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)

# Cor
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, posicao_stride, ctypes.c_void_p(3 * 4))
glEnableVertexAttribArray(1)

glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)
quadrantes = [
    (0,   300, 400, 300),
    (400, 300, 400, 300),
    (0,   0,   400, 300),
    (400, 0,   400, 300),
]


# LOOP
running = True
while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_1:
                        quadrantes = [
                            (400, 300, 400, 300),
                        ]
                    case pygame.K_2:
                        quadrantes = [
                            (0,   300, 400, 300),
                            (400, 300, 400, 300),
                            (0,   0,   400, 300),
                            (400, 0,   400, 300),
                        ]

        glClearColor(*SCREEN_COLOR)
        glClear(GL_COLOR_BUFFER_BIT)

        projection_loc = glGetUniformLocation(shader_program, "projection")

        glUseProgram(shader_program)
        glBindVertexArray(vao)
        glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection.T)

        for (x, y, w, h) in quadrantes:
            glViewport(x, y, w, h)
            glDrawArrays(GL_TRIANGLES, 0, 3)

        glBindVertexArray(0)
        glUseProgram(0)

        pygame.display.flip()
        clock.tick(FRAMERATE)

pygame.quit()