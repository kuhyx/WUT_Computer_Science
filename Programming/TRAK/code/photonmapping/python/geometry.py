#!/usr/bin/env python3
"""Vectors, photons and the two surfaces the standalone photon mapper traces.

Split out of `main.py` so each file stays under this repo's 250-line cap; the
classes are unchanged.
"""

from __future__ import annotations

import numpy as np

# A ray whose direction is this close to parallel with a plane never hits it.
_PARALLEL_EPSILON = 1e-6


# Define basic vector operations
class Vector3:
    """A 3D vector, with just the operations this renderer needs."""

    def __init__(self, x: float, y: float, z: float) -> None:
        """Store the three components."""
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: Vector3) -> Vector3:
        """Return the component-wise sum."""
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3) -> Vector3:
        """Return the component-wise difference."""
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> Vector3:
        """Return this vector scaled by `scalar`."""
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def dot(self, other: Vector3) -> float:
        """Return the dot product with `other`."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def norm(self) -> float:
        """Return the length of this vector."""
        return float(np.sqrt(self.dot(self)))

    def normalize(self) -> Vector3:
        """Return a new vector of unit length pointing the same way."""
        n = self.norm()
        return Vector3(self.x / n, self.y / n, self.z / n)


# Define the photon
class Photon:
    """A packet of light energy travelling in a straight line."""

    def __init__(
        self, position: Vector3, direction: Vector3, power: np.ndarray
    ) -> None:
        """Store where the photon is, where it is going, and what it carries."""
        self.position = position
        self.direction = direction
        self.power = power


# Define a simple sphere
class Sphere:
    """A sphere of uniform colour."""

    def __init__(self, center: Vector3, radius: float, color: np.ndarray) -> None:
        """Store the sphere's geometry and colour."""
        self.center = center
        self.radius = radius
        self.color = color

    def intersect(
        self, ray_origin: Vector3, ray_direction: Vector3
    ) -> tuple[float, Vector3, Vector3] | None:
        """Return the nearest hit as (distance, point, normal), or None."""
        # Solve quadratic equation for intersection
        oc = ray_origin - self.center
        a = ray_direction.dot(ray_direction)
        b = 2.0 * oc.dot(ray_direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return None  # No intersection
        t = (-b - np.sqrt(discriminant)) / (2.0 * a)
        if t < 0:
            t = (-b + np.sqrt(discriminant)) / (2.0 * a)
        if t < 0:
            return None
        hit_point = ray_origin + ray_direction * t
        normal = (hit_point - self.center).normalize()
        return (t, hit_point, normal)


# Define a simple plane
class Plane:
    """An infinite plane of uniform colour."""

    def __init__(self, point: Vector3, normal: Vector3, color: np.ndarray) -> None:
        """Store a point on the plane, its (normalised) normal, and its colour."""
        self.point = point
        self.normal = normal.normalize()
        self.color = color

    def intersect(
        self, ray_origin: Vector3, ray_direction: Vector3
    ) -> tuple[float, Vector3, Vector3] | None:
        """Return the nearest hit as (distance, point, normal), or None."""
        denom = self.normal.dot(ray_direction)
        if abs(denom) > _PARALLEL_EPSILON:
            t = (self.point - ray_origin).dot(self.normal) / denom
            if t >= 0:
                hit_point = ray_origin + ray_direction * t
                return (t, hit_point, self.normal)
        return None


Surface = Sphere | Plane
