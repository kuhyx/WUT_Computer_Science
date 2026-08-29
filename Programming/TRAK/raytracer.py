#!/usr/bin/env python3
"""Ray/geometry intersection and Phong shading for the `ray_tracing0` renderer.

These were nested closures inside `rendering.ray_trace`, which is what made
that one function 460 lines long. They are pure now: the scene and the light
constants are passed in rather than captured, so each can be read on its own.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

import numpy as np

# A scene object is a plain dict tagged with "type": "sphere" or "plane".
SceneObject = dict[str, Any]

# A ray whose direction is this close to parallel with a plane never hits it.
_PARALLEL_EPSILON = 1e-6

# Shadow and reflection rays start this far off the surface, so that the
# surface they just left does not intersect them at t=0.
SURFACE_OFFSET = 0.0001


@dataclass(frozen=True)
class Lighting:
    """The single point light and the Phong coefficients every surface uses."""

    position: np.ndarray
    color: np.ndarray
    ambient: float
    diffuse_c: float
    specular_c: float
    specular_k: int


def normalize(vector: np.ndarray) -> np.ndarray:
    """Scale `vector` to unit length, in place, and return it."""
    vector /= np.linalg.norm(vector)
    return vector


def intersect_plane(
    ray_origin: np.ndarray,
    ray_direction: np.ndarray,
    plane_point: np.ndarray,
    plane_normal: np.ndarray,
) -> float:
    """Distance along the ray to the plane, or +inf if it never reaches it."""
    denom = np.dot(ray_direction, plane_normal)
    if np.abs(denom) < _PARALLEL_EPSILON:
        return np.inf
    d = np.dot(plane_point - ray_origin, plane_normal) / denom
    if d < 0:
        return np.inf
    return float(d)


def calculate_sphere_intersection(a: float, b: float, c: float, disc: float) -> float:
    """Solve `a*t^2 + b*t + c` for the nearest root ahead of the ray origin.

    `disc` is the discriminant, passed in because the caller already has it.
    The root is taken via the numerically stable `q` form rather than the
    textbook quadratic formula, which loses precision when `b` dominates.
    """
    if disc > 0:
        distance_squared = np.sqrt(disc)
        q = (-b - distance_squared) / 2.0 if b < 0 else (-b + distance_squared) / 2.0
        t0 = q / a
        t1 = c / q
        t0, t1 = min(t0, t1), max(t0, t1)
        if t1 >= 0:
            return float(t1) if t0 < 0 else float(t0)
    return np.inf


def intersect_sphere(
    ray_origin: np.ndarray,
    ray_direction: np.ndarray,
    sphere_center: np.ndarray,
    sphere_radius: float,
) -> float:
    """Distance along the ray to the sphere, or +inf if it misses."""
    a = np.dot(ray_direction, ray_direction)
    origin_to_center = ray_origin - sphere_center
    b = 2 * np.dot(ray_direction, origin_to_center)
    radius_squared = sphere_radius * sphere_radius
    c = np.dot(origin_to_center, origin_to_center) - radius_squared
    disc = b * b - 4 * a * c
    return calculate_sphere_intersection(a, b, c, disc)


def intersect(
    ray_origin: np.ndarray, ray_direction: np.ndarray, object_: SceneObject
) -> float:
    """Dispatch to the plane or sphere intersection for `object_`."""
    if object_["type"] == "plane":
        return intersect_plane(
            ray_origin, ray_direction, object_["position"], object_["normal"]
        )
    return intersect_sphere(
        ray_origin, ray_direction, object_["position"], object_["radius"]
    )


def get_normal(object_: SceneObject, intersection_point: np.ndarray) -> np.ndarray:
    """Surface normal of `object_` at `intersection_point`."""
    if object_["type"] == "sphere":
        return normalize(intersection_point - object_["position"])
    if object_["type"] == "plane":
        return cast("np.ndarray", object_["normal"])
    msg = f"Unknown object type: {object_['type']}"
    raise ValueError(msg)


def get_color(object_: SceneObject, intersection_point: np.ndarray) -> np.ndarray:
    """Return the colour of `object_`: either a constant or a function of position."""
    color = object_["color"]
    if not hasattr(color, "__len__"):
        color = color(intersection_point)
    return cast("np.ndarray", color)


def find_intersection(
    scene: list[SceneObject], ray_origin: np.ndarray, ray_direction: np.ndarray
) -> tuple[float, int]:
    """Return the distance to the nearest hit and that object's scene index.

    The index is -1 when the ray hits nothing, in which case the distance is
    +inf and callers stop.
    """
    t = np.inf
    obj_idx = -1
    for index, object_ in enumerate(scene):
        t_obj = intersect(ray_origin, ray_direction, object_)
        if t_obj < t:
            t, obj_idx = t_obj, index
    return t, obj_idx


def is_shadowed(
    scene: list[SceneObject],
    lighting: Lighting,
    intersection_point: np.ndarray,
    normal: np.ndarray,
    obj_idx: int,
) -> bool:
    """Report whether anything but object `obj_idx` blocks the light here."""
    to_light = normalize(lighting.position - intersection_point)
    shadow_intersections = [
        intersect(intersection_point + normal * SURFACE_OFFSET, to_light, obj_sh)
        for k, obj_sh in enumerate(scene)
        if k != obj_idx
    ]
    return bool(shadow_intersections) and min(shadow_intersections) < np.inf


def compute_color(
    lighting: Lighting,
    object_: SceneObject,
    intersection_point: np.ndarray,
    normal: np.ndarray,
    ray_origin: np.ndarray,
) -> tuple[SceneObject, np.ndarray, np.ndarray, np.ndarray]:
    """Shade the hit with Blinn-Phong and return it alongside the hit geometry."""
    color = get_color(object_, intersection_point)
    to_light = normalize(lighting.position - intersection_point)
    to_origin = normalize(ray_origin - intersection_point)
    color_ray = lighting.ambient
    diffuse_intensity = object_.get("diffuse_c", lighting.diffuse_c) * max(
        np.dot(normal, to_light), 0
    )
    color_ray += diffuse_intensity * color
    half_vector = normalize(to_light + to_origin)
    specular_intensity = (
        object_.get("specular_c", lighting.specular_c)
        * max(np.dot(normal, half_vector), 0) ** lighting.specular_k
    )
    color_ray += specular_intensity * lighting.color
    return object_, intersection_point, normal, color_ray


def trace_ray(
    scene: list[SceneObject],
    lighting: Lighting,
    ray_origin: np.ndarray,
    ray_direction: np.ndarray,
) -> tuple[SceneObject, np.ndarray, np.ndarray, np.ndarray] | None:
    """Trace one ray and return its hit, or None if it misses or lands in shadow."""
    t, obj_idx = find_intersection(scene, ray_origin, ray_direction)
    if t == np.inf:
        return None
    object_ = scene[obj_idx]
    intersection_point = ray_origin + ray_direction * t
    normal = get_normal(object_, intersection_point)
    if is_shadowed(scene, lighting, intersection_point, normal, obj_idx):
        return None
    return compute_color(lighting, object_, intersection_point, normal, ray_origin)


def make_sphere(
    position: list[float], radius: float, color: np.ndarray
) -> SceneObject:
    """Build a sphere scene object."""
    return {
        "type": "sphere",
        "position": np.array(position),
        "radius": np.array(radius),
        "color": np.array(color),
        "reflection": 0.5,
    }


def make_plane(
    position: list[float],
    normal: list[float],
    color_a: np.ndarray,
    color_b: np.ndarray,
) -> SceneObject:
    """Build a plane scene object with a checkerboard of `color_a`/`color_b`."""
    return {
        "type": "plane",
        "position": np.array(position),
        "normal": np.array(normal),
        "color": lambda point: (
            color_a if (int(point[0] * 2) % 2) == (int(point[2] * 2) % 2) else color_b
        ),
        "diffuse_c": 0.75,
        "specular_c": 0.5,
        "reflection": 0.25,
    }
