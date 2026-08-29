#!/usr/bin/env python3
"""A two-pass photon mapper: scatter photons from the light, then gather them.

The first pass emits `num_photons` from the light and records every surface
they land on. The second pass shoots one camera ray per pixel and shades each
hit with direct light plus the photons gathered within `gather_radius`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import numpy as np
from photon_geometry import Photon, Plane, Sphere, Surface, Vector3

# Shadow rays start this far off the surface they were cast from.
_SHADOW_OFFSET = 1e-5

# Fraction of its power a photon keeps across one diffuse bounce.
_BOUNCE_ABSORPTION = 0.8


@dataclass
class Scene:
    """Everything the two passes share: the geometry, the light, the photons."""

    objects: list[Surface]
    rng: np.random.Generator
    light_position: Vector3
    light_power: np.ndarray
    gather_radius: float
    photon_map: list[tuple[Vector3, np.ndarray]]


def random_unit_vector(rng: np.random.Generator) -> Vector3:
    """Draw a direction uniformly over the sphere."""
    theta = rng.uniform(0, 2 * np.pi)
    z = rng.uniform(-1, 1)
    r = np.sqrt(1 - z * z)
    return Vector3(r * np.cos(theta), r * np.sin(theta), z)


def random_hemisphere_direction(rng: np.random.Generator, normal: Vector3) -> Vector3:
    """Draw a direction uniformly over the hemisphere around `normal`."""
    direction = random_unit_vector(rng)
    if direction.dot(normal) < 0:
        direction = Vector3(-direction.x, -direction.y, -direction.z)
    return direction


def nearest_hit(
    objects: list[Surface], ray_origin: Vector3, ray_direction: Vector3
) -> tuple[Surface, Vector3, Vector3] | None:
    """Return the closest surface the ray meets, with its point and normal."""
    closest_t = np.inf
    hit_object = None
    hit_info = None
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


def trace_photon(scene: Scene, photon: Photon, depth: int, max_depth: int) -> None:
    """Bounce one photon through the scene, recording every surface it lands on."""
    if depth > max_depth:
        return
    hit = nearest_hit(scene.objects, photon.position, photon.direction)
    if hit is not None:
        _, hit_point, normal = hit
        scene.photon_map.append((hit_point, photon.power))
        photon.position = hit_point
        photon.direction = random_hemisphere_direction(scene.rng, normal)
        photon.power = photon.power * _BOUNCE_ABSORPTION
        trace_photon(scene, photon, depth + 1, max_depth)


def emit_photons(scene: Scene, num_photons: int, max_depth: int) -> None:
    """Run the scatter pass: emit `num_photons` from the light and trace each."""
    for _ in range(num_photons):
        direction = random_unit_vector(scene.rng)
        power = scene.light_power / num_photons
        photon = Photon(scene.light_position, direction, power)
        trace_photon(scene, photon, 0, max_depth)


def compute_direct_light(scene: Scene, point: Vector3, normal: Vector3) -> np.ndarray:
    """Return the light arriving straight from the source, or black if shadowed."""
    direction_to_light = (scene.light_position - point).normalize()
    shadow_origin = point + normal * _SHADOW_OFFSET
    for obj in scene.objects:
        if obj.intersect(shadow_origin, direction_to_light):
            return np.array([0, 0, 0])
    intensity = max(0, normal.dot(direction_to_light))
    distance_squared = (scene.light_position - point).norm() ** 2
    return intensity * scene.light_power / (4 * np.pi * distance_squared)


def estimate_radiance(scene: Scene, point: Vector3, normal: Vector3) -> np.ndarray:
    """Gather the photons within `gather_radius` of `point` into a radiance."""
    accumulated_power = np.array([0.0, 0.0, 0.0])
    for photon_pos, photon_power in scene.photon_map:
        distance = (photon_pos - point).norm()
        if distance < scene.gather_radius:
            weight = max(0, normal.dot((photon_pos - point).normalize()))
            accumulated_power += photon_power * weight
    area = np.pi * scene.gather_radius**2
    return accumulated_power / area


def trace_ray(scene: Scene, ray_origin: Vector3, ray_direction: Vector3) -> np.ndarray:
    """Shade one camera ray with direct light plus gathered photons."""
    hit = nearest_hit(scene.objects, ray_origin, ray_direction)
    if hit is None:
        return np.array([0, 0, 0])
    hit_object, hit_point, normal = hit
    direct_light = compute_direct_light(scene, hit_point, normal)
    indirect_light = estimate_radiance(scene, hit_point, normal)
    return cast("np.ndarray", hit_object.color * (direct_light + indirect_light))


def render_photon_mapping(
    width: int, height: int, num_photons: int, max_depth: int, gather_radius: float
) -> np.ndarray:
    """Render the fixed red-sphere-over-grey-plane scene and return the image."""
    scene = Scene(
        objects=[
            Sphere(Vector3(0, 0, -5), 1.0, np.array([1, 0, 0])),  # Red sphere
            Plane(Vector3(0, -1, 0), Vector3(0, 1, 0), np.array([0.5, 0.5, 0.5])),
        ],
        rng=np.random.default_rng(),
        light_position=Vector3(-5, 5, -5),
        light_power=np.array([1, 1, 1]) * 1000,
        gather_radius=gather_radius,
        photon_map=[],
    )
    emit_photons(scene, num_photons, max_depth)

    aspect_ratio = width / height
    fov = np.pi / 3
    image = np.zeros((height, width, 3))
    for y in range(height):
        for x in range(width):
            px = (2 * (x + 0.5) / width - 1) * np.tan(fov / 2) * aspect_ratio
            py = (1 - 2 * (y + 0.5) / height) * np.tan(fov / 2)
            ray_direction = Vector3(px, py, -1).normalize()
            color = trace_ray(scene, Vector3(0, 0, 0), ray_direction)
            image[y, x, :] = np.clip(color, 0, 1)

    return image
