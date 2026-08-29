#!/usr/bin/env python3
"""View an OpenEXR environment map from the inside, on a GLUT-textured sphere.

Drag with the left mouse button to look around. The image is loaded as
32-bit float RGB and uploaded as a `GL_RGB32F` texture, so the high dynamic
range survives all the way to the driver.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path

import Imath
import OpenEXR
from OpenGL import GL, GLU, GLUT

logger = logging.getLogger(__name__)

# How far the camera turns per pixel of mouse drag.
_DEGREES_PER_PIXEL = 0.1


@dataclass
class ViewerState:
    """Camera orientation and mouse-drag state, mutated by the GLUT callbacks."""

    angle_x: float = 0.0
    angle_y: float = 0.0
    distance: float = 2.0
    last_x: int = 0
    last_y: int = 0
    left_down: bool = False


STATE = ViewerState()


def load_hdr_environment_map(filepath: str) -> tuple[int, int, bytes]:
    """Load an HDR environment map from an OpenEXR file.

    Returns the width, the height, and the pixels as interleaved float RGB,
    flipped vertically so that row 0 is the bottom row OpenGL expects.
    """
    if not Path(filepath).exists():
        msg = f"File not found: {filepath}"
        raise FileNotFoundError(msg)

    # Check file permissions
    if not os.access(filepath, os.R_OK):
        msg = f"File is not readable: {filepath}"
        raise PermissionError(msg)

    # Open the EXR file
    try:
        exr_file = OpenEXR.InputFile(filepath)
    except Exception as e:
        msg = f"Unable to open '{filepath}' for read: {e!s}"
        raise OSError(msg) from e

    # Get the image dimensions
    header = exr_file.header()
    dw = header["dataWindow"]
    width = dw.max.x - dw.min.x + 1
    height = dw.max.y - dw.min.y + 1

    # Define the channel names (R, G, B)
    channels = ["R", "G", "B"]

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
                hdr_image[index : index + 4] = channel_buffer[
                    (j * width + k) * 4 : (j * width + k + 1) * 4
                ]

    # Flip the image vertically
    flipped_hdr_image = bytearray(width * height * 3 * 4)
    row_size = width * 3 * 4
    for j in range(height):
        src_index = j * row_size
        dst_index = (height - 1 - j) * row_size
        flipped_hdr_image[dst_index : dst_index + row_size] = hdr_image[
            src_index : src_index + row_size
        ]

    return width, height, bytes(flipped_hdr_image)


def display_hdr_image(width: int, height: int, hdr_image: bytes) -> None:
    """Draw one frame: the environment map on the inside of a large sphere."""
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    # Enable texture mapping
    GL.glEnable(GL.GL_TEXTURE_2D)
    texture_id = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)

    # Set texture parameters
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

    # Load the texture
    GL.glTexImage2D(
        GL.GL_TEXTURE_2D,
        0,
        GL.GL_RGB32F,
        width,
        height,
        0,
        GL.GL_RGB,
        GL.GL_FLOAT,
        hdr_image,
    )

    # Set up the viewport and projection
    window_width = GLUT.glutGet(GLUT.GLUT_WINDOW_WIDTH)
    window_height = GLUT.glutGet(GLUT.GLUT_WINDOW_HEIGHT)
    GL.glViewport(0, 0, window_width, window_height)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GLU.gluPerspective(45.0, window_width / float(window_height), 0.1, 100.0)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()

    # Apply camera transformations
    GL.glTranslatef(0.0, 0.0, -STATE.distance)
    GL.glRotatef(STATE.angle_y, 1.0, 0.0, 0.0)
    GL.glRotatef(STATE.angle_x, 0.0, 1.0, 0.0)

    # Draw a textured sphere to simulate being inside the HDR environment
    quadric = GLU.gluNewQuadric()
    GLU.gluQuadricTexture(quadric, GL.GL_TRUE)
    GLU.gluSphere(quadric, 50.0, 50, 50)
    GLU.gluDeleteQuadric(quadric)

    # Disable texture mapping
    GL.glDisable(GL.GL_TEXTURE_2D)

    GLUT.glutSwapBuffers()


def mouse_motion(x: int, y: int) -> None:
    """Turn the camera by however far the pointer moved since the last event."""
    if STATE.left_down:
        dx = x - STATE.last_x
        dy = y - STATE.last_y
        STATE.angle_x += dx * _DEGREES_PER_PIXEL
        STATE.angle_y += dy * _DEGREES_PER_PIXEL
    STATE.last_x = x
    STATE.last_y = y
    GLUT.glutPostRedisplay()


def mouse_button(button: int, state: int, x: int, y: int) -> None:
    """Start a drag on left-button press and end it on release."""
    if button == GLUT.GLUT_LEFT_BUTTON:
        if state == GLUT.GLUT_DOWN:
            STATE.left_down = True
            # These two were assigned without a `global` declaration before, so
            # they went to locals and were thrown away: the first motion event
            # of every drag measured from wherever the previous drag ended.
            STATE.last_x = x
            STATE.last_y = y
        elif state == GLUT.GLUT_UP:
            STATE.left_down = False


def main(filepath: str) -> None:
    """Load `filepath` and hand control to the GLUT main loop."""
    try:
        width, height, hdr_map = load_hdr_environment_map(filepath)
    except OSError:
        # Covers the not-found, not-readable and unreadable-EXR cases above.
        # Anything else is a real fault and should surface as a traceback.
        logger.exception("Could not load '%s'", filepath)
        return

    logger.info("HDR Map Loaded. Dimensions: %s x %s", width, height)

    # Initialize GLUT and create window
    GLUT.glutInit()
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB | GLUT.GLUT_DEPTH)
    GLUT.glutInitWindowSize(800, 600)  # Set initial window size
    GLUT.glutCreateWindow(b"HDR Environment Map")

    # Set display callback
    GLUT.glutDisplayFunc(lambda: display_hdr_image(width, height, hdr_map))

    # Set mouse callbacks
    GLUT.glutMotionFunc(mouse_motion)
    GLUT.glutMouseFunc(mouse_button)

    # Start the GLUT main loop
    GLUT.glutMainLoop()


# Example usage
if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    main("lilienstein_4k.exr")
