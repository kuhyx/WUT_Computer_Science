from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

# Vertex shader
VERTEX_SHADER = """
#version 330
in vec3 position;
in vec3 color;
out vec3 vertexColor;
void main() {
    gl_Position = vec4(position, 1.0);
    vertexColor = color;
}
"""

# Fragment shader
FRAGMENT_SHADER = """
#version 330
in vec3 vertexColor;
out vec4 fragColor;
void main() {
    fragColor = vec4(vertexColor, 1.0);
}
"""

# Define vertices and colors
vertices = np.array([
    # Positions       # Colors
    0.0,  0.5, 0.0,    1.0, 0.0, 0.0,  # Top (red)
   -0.5, -0.5, 0.0,    0.0, 1.0, 0.0,  # Bottom-left (green)
    0.5, -0.5, 0.0,    0.0, 0.0, 1.0   # Bottom-right (blue)
], dtype=np.float32)

# Initialize OpenGL
def init():
    global shader, VAO

    # Compile shaders
    shader = compileProgram(
        compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )

    # Generate VAO and VBO
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * vertices.itemsize, None)
    glEnableVertexAttribArray(0)

    # Color attribute
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * vertices.itemsize, ctypes.c_void_p(3 * vertices.itemsize))
    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

# Render function
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(shader)
    glBindVertexArray(VAO)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glBindVertexArray(0)
    glUseProgram(0)
    glutSwapBuffers()

# Main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutCreateWindow(b"PyOpenGL Triangle")
    glutInitWindowSize(800, 600)
    glutDisplayFunc(display)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()
