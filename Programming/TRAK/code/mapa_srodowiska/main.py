import OpenEXR
import Imath
import os
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import OpenGL.GLU as glu
import math

# Camera parameters
camera_angle_x = 0.0
camera_angle_y = 0.0
camera_distance = 2.0
mouse_last_x = 0
mouse_last_y = 0
mouse_left_down = False

def load_hdr_environment_map(filepath):
    """
    Load an HDR environment map from an OpenEXR file.
    
    Args:
        filepath (str): Path to the HDR file.
        
    Returns:
        tuple: A tuple containing the width, height, and a bytes object representing the HDR environment map in RGB format.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    # Check file permissions
    if not os.access(filepath, os.R_OK):
        raise PermissionError(f"File is not readable: {filepath}")
    
    # Open the EXR file
    try:
        exr_file = OpenEXR.InputFile(filepath)
    except Exception as e:
        raise OSError(f"Unable to open '{filepath}' for read: {str(e)}")
    
    # Get the image dimensions
    header = exr_file.header()
    dw = header['dataWindow']
    width = dw.max.x - dw.min.x + 1
    height = dw.max.y - dw.min.y + 1

    # Define the channel names (R, G, B)
    channels = ['R', 'G', 'B']
    
    # Read the channel data
    channel_data = {
        channel: exr_file.channel(channel, Imath.PixelType(Imath.PixelType.FLOAT))
        for channel in channels
    }
    
    # Combine channel data into a single bytes object
    hdr_image = bytearray(width * height * 3 * 4)  # 3 channels, 4 bytes per float
    for i, channel in enumerate(channels):
        channel_buffer = channel_data[channel]
        for j in range(height):
            for k in range(width):
                index = (j * width + k) * 3 * 4 + i * 4
                hdr_image[index:index + 4] = channel_buffer[(j * width + k) * 4:(j * width + k + 1) * 4]

    # Flip the image vertically
    flipped_hdr_image = bytearray(width * height * 3 * 4)
    row_size = width * 3 * 4
    for j in range(height):
        src_index = j * row_size
        dst_index = (height - 1 - j) * row_size
        flipped_hdr_image[dst_index:dst_index + row_size] = hdr_image[src_index:src_index + row_size]

    return width, height, bytes(flipped_hdr_image)

def display_hdr_image(width, height, hdr_image):
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    
    # Enable texture mapping
    gl.glEnable(gl.GL_TEXTURE_2D)
    texture_id = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
    
    # Set texture parameters
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    
    # Load the texture
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB32F, width, height, 0, gl.GL_RGB, gl.GL_FLOAT, hdr_image)
    
    # Set up the viewport and projection
    gl.glViewport(0, 0, glut.glutGet(glut.GLUT_WINDOW_WIDTH), glut.glutGet(glut.GLUT_WINDOW_HEIGHT))
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluPerspective(45.0, glut.glutGet(glut.GLUT_WINDOW_WIDTH) / float(glut.glutGet(glut.GLUT_WINDOW_HEIGHT)), 0.1, 100.0)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    
    # Apply camera transformations
    gl.glTranslatef(0.0, 0.0, -camera_distance)
    gl.glRotatef(camera_angle_y, 1.0, 0.0, 0.0)
    gl.glRotatef(camera_angle_x, 0.0, 1.0, 0.0)
    
    # Draw a textured sphere to simulate being inside the HDR environment
    quadric = glu.gluNewQuadric()
    glu.gluQuadricTexture(quadric, gl.GL_TRUE)
    glu.gluSphere(quadric, 50.0, 50, 50)
    glu.gluDeleteQuadric(quadric)
    
    # Disable texture mapping
    gl.glDisable(gl.GL_TEXTURE_2D)
    
    glut.glutSwapBuffers()

def mouse_motion(x, y):
    global mouse_last_x, mouse_last_y, camera_angle_x, camera_angle_y
    if mouse_left_down:
        dx = x - mouse_last_x
        dy = y - mouse_last_y
        camera_angle_x += dx * 0.1
        camera_angle_y += dy * 0.1
    mouse_last_x = x
    mouse_last_y = y
    glut.glutPostRedisplay()

def mouse_button(button, state, x, y):
    global mouse_left_down
    if button == glut.GLUT_LEFT_BUTTON:
        if state == glut.GLUT_DOWN:
            mouse_left_down = True
            mouse_last_x = x
            mouse_last_y = y
        elif state == glut.GLUT_UP:
            mouse_left_down = False

def main(filepath):    
    try:
        width, height, hdr_map = load_hdr_environment_map(filepath)
        print("HDR Map Loaded. Dimensions:", width, "x", height)
        
        # Initialize GLUT and create window
        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH)
        glut.glutInitWindowSize(800, 600)  # Set initial window size
        glut.glutCreateWindow(b"HDR Environment Map")
        
        # Set display callback
        glut.glutDisplayFunc(lambda: display_hdr_image(width, height, hdr_map))
        
        # Set mouse callbacks
        glut.glutMotionFunc(mouse_motion)
        glut.glutMouseFunc(mouse_button)
        
        # Start the GLUT main loop
        glut.glutMainLoop()
    except Exception as e:
        print(e)

# Example usage
if __name__ == "__main__":
    filepath = "lilienstein_4k.exr"
    main(filepath)
