#!/usr/bin/env python3
"""Renders an image using raytracing.

The geometry and shading live in `raytracer`; what is left here is the scene
this lab builds (a checkerboard plane and a row of spheres) and the pixel loop
that shoots one primary ray per pixel and reflects it up to `DEPTH_MAX` times.
"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from raytracer import (
    SURFACE_OFFSET,
    Lighting,
    SceneObject,
    make_plane,
    make_sphere,
    normalize,
    trace_ray,
)

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)

# Default light and material parameters.
AMBIENT = 0.05
DIFFUSE_C = 1.0
SPECULAR_C = 1.0
SPECULAR_K = 50

DEPTH_MAX = 5  # Maximum number of light reflections.

# Progress is logged every this many pixel columns.
_PROGRESS_EVERY = 10


def build_scene(num_spheres: int) -> list[SceneObject]:
    """Lay out a checkerboard plane and `num_spheres` spheres in a receding row."""
    color_plane0 = 1.0 * np.ones(3)
    color_plane1 = 0.0 * np.ones(3)
    scene = [make_plane([0.0, -0.5, 0.0], [0.0, 1.0, 0.0], color_plane0, color_plane1)]

    base_radius = 1 / np.sqrt(num_spheres)  # Im więcej kul, tym mniejsze
    base_distance = 4.5 / num_spheres

    for i in range(num_spheres):
        # Wyliczanie pozycji każdej kuli
        x = (i - num_spheres // 2) * base_distance
        y = 0.1
        z = 1.0 + i * 0.5

        # Dynamiczny kolor (gradient na podstawie indeksu)
        color = np.array([i / num_spheres, (num_spheres - i) / num_spheres, 0.5])

        # Dodanie kuli do sceny
        scene.append(make_sphere([x, y, z], base_radius, color))

    return scene


def ray_trace(
    num_spheres: int,
    _environment: str,
    image_width: int = 400,
    image_height: int = 300,
    output_file: str | Path = "fig.png",
) -> None:
    """Render `num_spheres` spheres over a checkerboard and write `output_file`.

    `_environment` is accepted for symmetry with the other two algorithms in
    `main.py` and ignored: this renderer has no environment map.
    """
    scene = build_scene(num_spheres)
    lighting = Lighting(
        position=np.array([5.0, 5.0, -10.0]),
        color=np.ones(3),
        ambient=AMBIENT,
        diffuse_c=DIFFUSE_C,
        specular_c=SPECULAR_C,
        specular_k=SPECULAR_K,
    )

    color = np.zeros(3)  # Current color.
    camera_origin = np.array([0.0, 0.35, -1.0])  # Camera.
    camera_target = np.array([0.0, 0.0, 0.0])  # Camera pointing to.
    img = np.zeros((image_height, image_width, 3))

    aspect = float(image_width) / image_height
    # Screen coordinates: x0, y0, x1, y1.
    screen = (-1.0, -1.0 / aspect + 0.25, 1.0, 1.0 / aspect + 0.25)

    render_time = time.time()
    reflections = 0
    rays = 0
    primary_rays = 0
    # Loop through all pixels.
    for i, x in enumerate(np.linspace(screen[0], screen[2], image_width)):
        if i % _PROGRESS_EVERY == 0:
            logger.info("%s %%", round(i / float(image_width) * 100, 2))
        for j, y in enumerate(np.linspace(screen[1], screen[3], image_height)):
            color[:] = 0
            camera_target[:2] = (x, y)
            ray_origin = camera_origin
            ray_direction = normalize(camera_target - camera_origin)
            depth = 0
            reflection = 1.0
            primary_rays += 1
            # Loop through initial and secondary rays.
            while depth < DEPTH_MAX:
                traced = trace_ray(scene, lighting, ray_origin, ray_direction)
                rays += 1
                if not traced:
                    break
                reflections += 1
                obj, hit_point, hit_normal, color_ray = traced
                # Reflection: create a new ray.
                ray_origin = hit_point + hit_normal * SURFACE_OFFSET
                ray_direction = normalize(
                    ray_direction - 2 * np.dot(ray_direction, hit_normal) * hit_normal
                )
                depth += 1
                color += reflection * color_ray
                reflection *= obj.get("reflection", 1.0)
            img[image_height - j - 1, i, :] = np.clip(color, 0, 1)
    render_time = time.time() - render_time

    plt.imsave(output_file, img)
    logger.info(
        "Image saved as %s\nresolution: %sx%s\nrender time: %s s\nreflections: %s\n"
        "rays (initial): %s\nrays (secondary): %s\nrays (total): %s",
        output_file,
        image_width,
        image_height,
        round(render_time, 2),
        reflections,
        primary_rays,
        rays - primary_rays,
        rays,
    )
