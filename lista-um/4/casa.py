import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

SCREEN_SIZE = (800, 600)
SCREEN_COLOR = (0.3, 0.3, 0.3, 1.0)
FRAMERATE = 60

# Shaders
VERTEX_SHADER = """
#version 330
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
out vec3 Color;
void main() {
    gl_Position = vec4(aPos, 1.0);
    Color = aColor;
}
"""

FRAGMENT_SHADER = """
#version 330
in vec3 Color;
out vec4 FragColor;
void main() {
    FragColor = vec4(Color, 1.0);
}
"""

def criar_vao_triangulo(v1, v2, v3, cor):
    """Cria um VAO para um único triângulo com cor sólida."""
    dados = np.array([
        v1[0], v1[1], v1[2], cor[0], cor[1], cor[2],
        v2[0], v2[1], v2[2], cor[0], cor[1], cor[2],
        v3[0], v3[1], v3[2], cor[0], cor[1], cor[2]
    ], dtype=np.float32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, dados.nbytes, dados, GL_STATIC_DRAW)

    # posição
    stride = 6 * 4
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # cor
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * 4))
    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    return vao, 3

def criar_vao_retangulo(x1, y1, x2, y2, z, cor):
    # Primeiro triângulo: (x1,y1) -> (x2,y1) -> (x2,y2)
    # Segundo triângulo: (x1,y1) -> (x2,y2) -> (x1,y2)
    dados = np.array([
        x1, y1, z, cor[0], cor[1], cor[2],
        x2, y1, z, cor[0], cor[1], cor[2],
        x2, y2, z, cor[0], cor[1], cor[2],
        x1, y1, z, cor[0], cor[1], cor[2],
        x2, y2, z, cor[0], cor[1], cor[2],
        x1, y2, z, cor[0], cor[1], cor[2]
    ], dtype=np.float32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, dados.nbytes, dados, GL_STATIC_DRAW)

    stride = 6 * 4
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * 4))
    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    return vao, 6

# Pygame
pygame.init()
pygame.display.set_mode(SCREEN_SIZE, pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

# Compilação shaders
try:
    program = compileProgram(
        compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )
except RuntimeError as e:
    print(f"Erro nos shaders: {e}")
    pygame.quit()
    exit()

# Definição coordenadas
telhado_vao, telhado_count = criar_vao_triangulo(
    (-0.5, 0.3, 0.0), (0.5, 0.3, 0.0), (0.0, 0.8, 0.0), (1.0, 0.0, 0.0)
)

corpo_vao, corpo_count = criar_vao_retangulo(-0.5, -0.5, 0.5, 0.3, 0.0, (1.0, 1.0, 0.0))

porta_vao, porta_count = criar_vao_retangulo(-0.15, -0.5, 0.15, -0.15, 0.0, (0.5, 0.25, 0.0))

janela_esq_vao, janela_esq_count = criar_vao_retangulo(-0.4, -0.15, -0.25, 0.05, 0.0, (0.5, 0.8, 1.0))

janela_dir_vao, janela_dir_count = criar_vao_retangulo(0.25, -0.15, 0.4, 0.05, 0.0, (0.5, 0.8, 1.0))

# Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    glClearColor(*SCREEN_COLOR)
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(program)

    glBindVertexArray(telhado_vao)
    glDrawArrays(GL_TRIANGLES, 0, telhado_count)

    glBindVertexArray(corpo_vao)
    glDrawArrays(GL_TRIANGLES, 0, corpo_count)

    glBindVertexArray(porta_vao)
    glDrawArrays(GL_TRIANGLES, 0, porta_count)

    glBindVertexArray(janela_esq_vao)
    glDrawArrays(GL_TRIANGLES, 0, janela_esq_count)

    glBindVertexArray(janela_dir_vao)
    glDrawArrays(GL_TRIANGLES, 0, janela_dir_count)

    glBindVertexArray(0)
    glUseProgram(0)

    pygame.display.flip()
    clock.tick(FRAMERATE)

pygame.quit()