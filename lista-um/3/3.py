import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

SCREEN_SIZE = (800, 600)
SCREEN_COLOR = (0.3, 0.3, 0.3, 1.0)
WINDOW_CREATION_FLAGS = pygame.OPENGL | pygame.DOUBLEBUF
FRAMERATE = 60

# DEFINIÇÃO SHADERS
VERTEX_SHADER_SOURCE = """
#version 330
layout (location = 0) in vec3 aPos;   // Posição do vértice (location = 0)
layout (location = 1) in vec3 aColor; // Cor do vértice (location = 1)
out vec3 Color;                       // Envia a cor interpolada para o Fragment Shader
void main() {
    gl_Position = vec4(aPos, 1.0);    // Projeção ortográfica padrão (-1 a 1)
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
# P1 (Vermelho), P2 (Verde), P3 (Azul)
dados_vertices = np.array([
    #  X,    Y,   Z,   R,   G,   B
    -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
     0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
     0.0,  0.5, 0.0, 0.0, 0.0, 1.0
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

# LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    glClearColor(*SCREEN_COLOR)
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader_program)      # Ativa nossos shaders
    glBindVertexArray(vao)            # Ativa o VAO
    glDrawArrays(GL_TRIANGLES, 0, 3)  # Desenha o triângulo
    glBindVertexArray(0)              # Desativa (boa prática)
    glUseProgram(0)                   # Desativa (boa prática)

    pygame.display.flip()
    clock.tick(FRAMERATE)

pygame.quit()