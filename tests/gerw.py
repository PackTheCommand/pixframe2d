import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import *

# Initialize Pygame
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Create a Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)

# Vertex shader code
vertex_shader_code = """
    attribute vec2 position;
    void main() {
        gl_Position = vec4(position, 0.0, 1.0);
    }
"""

# Fragment shader code for darkness effect
fragment_shader_code = """
    uniform float darkness;
    void main() {
        gl_FragColor = vec4(0.0, 0.0, 0.0, darkness);
    }
"""

# Compile the shaders
vertex_shader = compileShader(vertex_shader_code, GL_VERTEX_SHADER)
fragment_shader = compileShader(fragment_shader_code, GL_FRAGMENT_SHADER)

# Create a shader program
shader_program = glCreateProgram()
glAttachShader(shader_program, vertex_shader)
glAttachShader(shader_program, fragment_shader)
glLinkProgram(shader_program)
glUseProgram(shader_program)

# Set up a quad to cover the entire screen
vertices = [-1, -1, 1, -1, -1, 1, 1, 1]
vertices = (GLfloat * len(vertices))(*vertices)
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, vertices, GL_STATIC_DRAW)

position = glGetAttribLocation(shader_program, "position")
glEnableVertexAttribArray(position)
glVertexAttribPointer(position, 2, GL_FLOAT, GL_FALSE, 0, None)

# Main loop
running = True
darkness = 0.0  # Adjust this value to control darkness (0.0 to 1.0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glUseProgram(shader_program)
    glUniform1f(glGetUniformLocation(shader_program, "darkness"), darkness)

    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
    pygame.display.flip()

# Clean up
glDeleteProgram(shader_program)
glDeleteBuffers(1, [vbo])
pygame.quit()