#!/usr/bin/env python3
"""Standalone photon mapper: scatter photons from the light, then gather them.

The lab version, kept whole: the scene, the light and the photon map are
module-level state, and running the file emits photons, renders a 100x100
image and shows it. `Programming/TRAK/photon_mapping.py` is the later
parameterised rewrite of the same algorithm.
"""

from __future__ import annotations

import logging
import time
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from geometry import Photon, Plane, Sphere, Surface, Vector3

logger = logging.getLogger(__name__)

# Shadow rays start this far off the surface they were cast from.
_SHADOW_OFFSET = 1e-5

# Fraction of its power a photon keeps across one diffuse bounce.
_BOUNCE_ABSORPTION = 0.8

# One generator for the whole module, matching the module-level scene below.
_rng = np.random.default_rng()

# Scene setup
sphere = Sphere(Vector3(0, 0, -5), 1.0, np.array([1, 0, 0]))  # Red sphere
plane = Plane(
    Vector3(0, -1, 0), Vector3(0, 1, 0), np.array([0.5, 0.5, 0.5])
)  # Gray plane

objects: list[Surface] = [sphere, plane]

# Light source
light_position = Vector3(-5, 5, -5)
light_power = np.array([1, 1, 1]) * 1000  # Intense white light

# Photon map
photon_map: list[tuple[Vector3, np.ndarray]] = []

# Parameters
num_photons = 10000  # Number of photons to emit
max_depth = 5  # Maximum number of bounces
gather_radius = 0.5  # Radius for radiance estimation


def random_unit_vector() -> Vector3:
    """Draw a direction uniformly over the sphere."""
    theta = _rng.uniform(0, 2 * np.pi)
    z = _rng.uniform(-1, 1)
    r = np.sqrt(1 - z * z)
    return Vector3(r * np.cos(theta), r * np.sin(theta), z)


def random_hemisphere_direction(normal: Vector3) -> Vector3:
    """Draw a direction uniformly over the hemisphere around `normal`."""
    direction = random_unit_vector()
    if direction.dot(normal) < 0:
        direction = Vector3(-direction.x, -direction.y, -direction.z)
    return direction


def nearest_hit(
    ray_origin: Vector3, ray_direction: Vector3
) -> tuple[Surface, Vector3, Vector3] | None:
    """Return the closest surface the ray meets, with its point and normal."""
    closest_t = np.inf
    hit_object = None
    hit_info = None
    # Find the nearest intersection
    for obj in objects:
        result = obj.intersect(ray_origin, ray_direction)
        if result:
            t, hit_point, normal = result
            if t < closest_t:
                closest_t = t
                hit_object = obj
                hit_info = (hit_point, normal)
    if hit_object is None or hit_info is None:
        return None
    return (hit_object, hit_info[0], hit_info[1])


def trace_photon(photon: Photon, depth: int) -> int:
    """Bounce one photon, recording each landing, and return the traces made.

    The count is what the original `global PHOTONS` accumulated: one per call,
    bounces included.
    """
    if depth > max_depth:
        return 1
    hit = nearest_hit(photon.position, photon.direction)
    if hit is None:
        return 1
    _, hit_point, normal = hit
    photon_map.append((hit_point, photon.power))
    # Diffuse reflection
    photon.position = hit_point
    photon.direction = random_hemisphere_direction(normal)
    # Absorb some power
    photon.power = photon.power * _BOUNCE_ABSORPTION  # Simple absorption
    return 1 + trace_photon(photon, depth + 1)


def emit_photons() -> int:
    """Emit `num_photons` from the light and return the total traces made."""
    traces = 0
    for _ in range(num_photons):
        # Emit photons in random directions from the light source
        direction = random_unit_vector()
        power = light_power / num_photons
        traces += trace_photon(Photon(light_position, direction, power), 0)
    return traces


def compute_direct_light(point: Vector3, normal: Vector3) -> np.ndarray:
    """Return the light arriving straight from the source, or black if shadowed."""
    # Simple Lambertian reflection from light source
    direction_to_light = (light_position - point).normalize()
    # Shadow ray
    shadow_origin = point + normal * _SHADOW_OFFSET
    for obj in objects:
        if obj.intersect(shadow_origin, direction_to_light):
            return np.array([0, 0, 0])
    intensity = max(0, normal.dot(direction_to_light))
    return intensity * light_power / (4 * np.pi * (light_position - point).norm() ** 2)


def estimate_radiance(point: Vector3, normal: Vector3) -> np.ndarray:
    """Gather the photons within `gather_radius` of `point` into a radiance."""
    accumulated_power = np.array([0.0, 0.0, 0.0])
    for photon_pos, photon_power in photon_map:
        distance = (photon_pos - point).norm()
        if distance < gather_radius:
            weight = max(0, normal.dot((photon_pos - point).normalize()))
            accumulated_power += photon_power * weight
    area = np.pi * gather_radius**2
    return accumulated_power / (area * num_photons)


def trace_ray(ray_origin: Vector3, ray_direction: Vector3) -> np.ndarray:
    """Shade one camera ray with direct light plus gathered photons."""
    hit = nearest_hit(ray_origin, ray_direction)
    if hit is None:
        return np.array([0, 0, 0])  # Background color
    hit_object, hit_point, normal = hit
    direct_light = compute_direct_light(hit_point, normal)
    indirect_light = estimate_radiance(hit_point, normal)
    return cast("np.ndarray", hit_object.color * (direct_light + indirect_light))


def render_image(width: int, height: int) -> np.ndarray:
    """Shoot one camera ray per pixel and return the `height` x `width` image."""
    aspect_ratio = width / height
    fov = np.pi / 3  # 60 degrees field of view
    image = np.zeros((height, width, 3))
    for y in range(height):
        for x in range(width):
            # Convert pixel coordinate to camera ray
            px = (2 * (x + 0.5) / width - 1) * np.tan(fov / 2) * aspect_ratio
            py = (1 - 2 * (y + 0.5) / height) * np.tan(fov / 2)
            ray_direction = Vector3(px, py, -1).normalize()
            image[y, x, :] = np.clip(trace_ray(Vector3(0, 0, 0), ray_direction), 0, 1)
    return image


def main() -> None:
    """Emit photons, render the image and show it."""
    logger.info("Emitting photons...")
    photon_traces = emit_photons()

    logger.info("Rendering image...")
    width = 100
    height = 100
    t0 = time.time()
    image = render_image(width, height)

    logger.info(
        "Render Took: %ss\nresolution: %sx%s\nphotons (emitted): %s\n"
        "photons (reflected): %s\nphotons (total): %s\nrays: %s",
        round(time.time() - t0, 2),
        width,
        height,
        num_photons,
        photon_traces - num_photons,
        photon_traces,
        width * height,
    )

    # Display the image
    plt.imshow(image)
    plt.axis("off")
    plt.show()


# Main execution
if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    main()
