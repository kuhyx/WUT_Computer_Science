#!/usr/bin/env python3
""" Renders an image using raytracing """
import numpy as np
import matplotlib.pyplot as plt

IMAGE_WIDTH = 400
IMAGE_HEIGHT = 300


def normalize(vector):
    """
    Normalize a vector.

    Parameters:
    vector (numpy.ndarray): The input vector to be normalized.

    Returns:
    numpy.ndarray: The normalized vector.
    """
    vector /= np.linalg.norm(vector)
    return vector


def intersect_plane(ray_origin, ray_direction, plane_point, plane_normal):
    """
    Calculate the intersection of a ray with a plane.

    Parameters:
    ray_origin (numpy.ndarray): A 3D point representing the origin of the ray.
    ray_direction (numpy.ndarray): A normalized 3D vector representing the
    direction of the ray.
    plane_point (numpy.ndarray): A 3D point representing a point on the plane.
    plane_normal (numpy.ndarray): A normalized 3D vector representing
    the normal of the plane.

    Returns:
    float: The distance from the origin ray_origin to the intersection
    point with the plane.
           Returns +inf if there is no intersection or if the intersection is
           behind the origin.
    """
    denom = np.dot(ray_direction, plane_normal)
    if np.abs(denom) < 1e-6:
        return np.inf
    d = np.dot(plane_point - ray_origin, plane_normal) / denom
    if d < 0:
        return np.inf
    return d


def intersect_sphere(ray_origin, ray_direction, sphere_center, sphere_radius):
    """
    Calculate the intersection of a ray with a sphere.

    Parameters:
    ray_origin (numpy.ndarray): A 3D point representing the origin of the ray.
    ray_direction (numpy.ndarray): A normalized 3D vector representing the
    direction of the ray.
    sphere_center (numpy.ndarray): A 3D point representing
    the center of the sphere.
    sphere_radius (float): The radius of the sphere.

    Returns:
    float: The distance from the origin ray_origin to the intersection
    point with the sphere.
           Returns +inf if there is no intersection or if the intersection is
           behind the origin.
    """
    a = np.dot(ray_direction, ray_direction)
    origin_to_center = ray_origin - sphere_center
    b = 2 * np.dot(ray_direction, origin_to_center)
    radius_squared = sphere_radius * sphere_radius
    c = np.dot(origin_to_center, origin_to_center) - radius_squared
    disc = b * b - 4 * a * c
    return calculate_sphere_intersection(a, b, c, disc)


def calculate_sphere_intersection(a, b, c, disc):
    """
    Calculate the
    intersection distance of a ray with a sphere using the quadratic formula.

    Parameters:
    a (float): Coefficient of t^2 in the quadratic equation.
    b (float): Coefficient of t in the quadratic equation.
    c (float): Constant term in the quadratic equation.
    disc (float): Discriminant of the quadratic equation.

    Returns:
    float:
    The distance from the origin to the intersection point with the sphere.
    Returns +inf if there is no intersection
    or if the intersection is behind the origin.
    """
    if disc > 0:
        distance_squared = np.sqrt(disc)
        # q is used to find the roots of the quadratic equation
        if b < 0:
            q = (-b - distance_squared) / 2.0
        else:
            q = (-b + distance_squared) / 2.0
        t0 = q / a
        t1 = c / q
        t0, t1 = min(t0, t1), max(t0, t1)
        if t1 >= 0:
            return t1 if t0 < 0 else t0
    return np.inf


def intersect(ray_origin, ray_direction, object_):
    """
    Calculate the intersection of a ray with an object.

    Parameters:
    ray_origin (numpy.ndarray): A 3D point representing the origin of the ray.
    ray_direction (numpy.ndarray): A normalized 3D vector representing the
    direction of the ray.
    obj (dict): A dictionary representing the object with keys
    'type', 'position', 'normal' (for planes), and 'radius' (for spheres).

    Returns:
    float: The distance from the origin ray_origin to the intersection
    point with the object.
           Returns +inf if there is no intersection or if the intersection is
           behind the origin.
    """
    if object_['type'] == 'plane':
        return intersect_plane(ray_origin, ray_direction,
                               object_['position'], object_['normal'])
    # object_['type'] == 'sphere':
    return intersect_sphere(ray_origin, ray_direction,
                            object_['position'], object_['radius'])


def get_normal(object_, intersection_point):
    """
    Calculate the normal at the intersection point on the object.

    Parameters:
    obj (dict): A dictionary representing the object with keys
    'type' and 'position'.
    intersection_point (numpy.ndarray): A 3D point representing the
    intersection point on the object.

    Returns:
    numpy.ndarray: The normal vector at the intersection point.
    """
    if object_['type'] == 'sphere':
        normal = normalize(intersection_point - object_['position'])
    elif object_['type'] == 'plane':
        normal = object_['normal']
    else:
        raise ValueError(f"Unknown object type: {object_['type']}")
    return normal


def get_color(object_, intersection_point):
    """
    Get the color of the object at the intersection point.

    Parameters:
    object_ (dict): A dictionary representing the object with a key 'color'.
    intersection_point (numpy.ndarray): A 3D point representing the
    intersection point on the object.

    Returns:
    numpy.ndarray: The color of the object at the intersection point.
    """
    color = object_['color']
    if not hasattr(color, '__len__'):
        color = color(intersection_point)
    return color


def trace_ray(ray_origin, ray_direction):
    """
    Trace a ray and find the color at the intersection point.

    Parameters:
    ray_origin (numpy.ndarray): A 3D point representing the origin of the ray.
    ray_direction (numpy.ndarray):
    A normalized 3D vector representing the direction of the ray.

    Returns:
    tuple: A tuple containing the object,
    intersection point, normal at the intersection,
    and the color at the intersection point.
    Returns None if there is no intersection.
    """
    t, obj_idx = find_intersection(ray_origin, ray_direction)
    if t == np.inf:
        return None
    object_, intersection_point = get_intersection_details(
        ray_origin, ray_direction, t, obj_idx)
    normal, color = get_normal(object_, intersection_point), get_color(
        object_, intersection_point)
    if is_shadowed(intersection_point, normal, obj_idx):
        return None
    return compute_color(
        object_, intersection_point, normal, color, ray_origin)


def find_intersection(ray_origin, ray_direction):
    """
    Find the intersection of a ray with the objects in the scene.

    Parameters:
    ray_origin (numpy.ndarray): A 3D point representing the origin of the ray.
    ray_direction (numpy.ndarray):
    A normalized 3D vector representing the direction of the ray.

    Returns:
    tuple: A tuple containing the distance to the intersection point
    and the index of the intersected object.
    """
    t = np.inf
    obj_idx = -1
    for index, object_ in enumerate(scene):
        t_obj = intersect(ray_origin, ray_direction, object_)
        if t_obj < t:
            t, obj_idx = t_obj, index
    return t, obj_idx


def get_intersection_details(ray_origin, ray_direction, t, obj_idx):
    """
    Get the details of the intersection point on the object.

    Parameters:
    ray_origin (numpy.ndarray): A 3D point representing the origin of the ray.
    ray_direction (numpy.ndarray):
    A normalized 3D vector representing the direction of the ray.
    t (float): The distance to the intersection point.
    obj_idx (int): The index of the intersected object in the scene.

    Returns:
    tuple: A tuple containing the intersected object
    and the intersection point.
    """
    object_ = scene[obj_idx]
    intersection_point = ray_origin + ray_direction * t
    return object_, intersection_point


def is_shadowed(intersection_point, normal, obj_idx):
    """
    Determine if the intersection point is in shadow.

    Parameters:
    intersection_point (numpy.ndarray):
    A 3D point representing the intersection point on the object.
    normal (numpy.ndarray): The normal vector at the intersection point.
    obj_idx (int): The index of the intersected object in the scene.

    Returns:
    bool: True if the intersection point is in shadow, False otherwise.
    """
    to_light = normalize(L - intersection_point)
    shadow_intersections = [intersect(
        intersection_point + normal * .0001, to_light, obj_sh)
                            for k, obj_sh in enumerate(scene) if k != obj_idx]
    return shadow_intersections and min(shadow_intersections) < np.inf


def compute_color(object_, intersection_point, normal, color, ray_origin):
    """
    Compute the color at the intersection point using shading techniques.

    Parameters:
    object_ (dict): A dictionary representing the intersected object.
    intersection_point (numpy.ndarray):
    A 3D point representing the intersection point on the object.
    normal (numpy.ndarray): The normal vector at the intersection point.
    color (numpy.ndarray): The base color of the object.
    ray_origin (numpy.ndarray): A 3D point representing the origin of the ray.

    Returns:
    tuple:
    A tuple containing the intersected object, intersection point, normal,
    and the computed color.
    """
    to_light = normalize(L - intersection_point)
    to_origin = normalize(ray_origin - intersection_point)
    color_ray = AMBIENT
    diffuse_intensity = object_.get('diffuse_c', DIFFUSE_C) * max(
        np.dot(normal, to_light), 0)
    color_ray += diffuse_intensity * color
    half_vector = normalize(to_light + to_origin)
    specular_intensity = object_.get('specular_c', SPECULAR_C) * max(
        np.dot(normal, half_vector), 0) ** SPECULAR_K
    color_ray += specular_intensity * color_light
    return object_, intersection_point, normal, color_ray


def add_sphere(position, radius, color):
    """
    Create a dictionary representing a sphere object.

    Parameters:
    position (list or numpy.ndarray):
    A 3D point representing the position of the sphere.
    radius (float): The radius of the sphere.
    color (list or numpy.ndarray): The color of the sphere.

    Returns:
    dict: A dictionary representing the sphere object.
    """
    return {
        'type': 'sphere',
        'position': np.array(position),
        'radius': np.array(radius),
        'color': np.array(color),
        'reflection': .5
    }


def add_plane(position, normal):
    """
    Create a dictionary representing a plane object.

    Parameters:
    position (list or numpy.ndarray):
    A 3D point representing a point on the plane.
    normal (list or numpy.ndarray):
    A normalized 3D vector representing the normal of the plane.

    Returns:
    dict: A dictionary representing the plane object.
    """
    return {
        'type': 'plane',
        'position': np.array(position),
        'normal': np.array(normal),
        'color': lambda M: (color_plane0
                            if (int(M[0] * 2) % 2) == (int(M[2] * 2) % 2)
                            else color_plane1),
        'diffuse_c': .75,
        'specular_c': .5,
        'reflection': .25
    }


# List of objects.
color_plane0 = 1. * np.ones(3)
color_plane1 = 0. * np.ones(3)
scene = [add_sphere([.75, .1, 1.], .6, [1., 0., 0.]),
         add_sphere([-.75, .1, 2.25], .6, [0., 1., 0.]),
         add_sphere([-2.75, .1, 3.5], .6, [0., 0., 1.]),
         add_plane([0., -.5, 0.], [0., 1., 0.]),
         ]

# Light position and color.
L = np.array([5., 5., -10.])
color_light = np.ones(3)

# Default light and material parameters.
AMBIENT = .05
DIFFUSE_C = 1.
SPECULAR_C = 1.
SPECULAR_K = 50

DEPTH_MAX = 5  # Maximum number of light reflections.
col = np.zeros(3)  # Current color.
camera_origin = np.array([0., 0.35, -1.])  # Camera.
Q = np.array([0., 0., 0.])  # Camera pointing to.
img = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 3))

r = float(IMAGE_WIDTH) / IMAGE_HEIGHT
# Screen coordinates: x0, y0, x1, y1.
S = (-1., -1. / r + .25, 1., 1. / r + .25)

# Loop through all pixels.
for i, x in enumerate(np.linspace(S[0], S[2], IMAGE_WIDTH)):
    if i % 10 == 0:
        print(i / float(IMAGE_WIDTH) * 100, "%")
    for j, y in enumerate(np.linspace(S[1], S[3], IMAGE_HEIGHT)):
        col[:] = 0
        Q[:2] = (x, y)
        D = normalize(Q - camera_origin)
        DEPTH = 0
        rayO, rayD = camera_origin, D
        REFLECTION = 1.
        # Loop through initial and secondary rays.
        while DEPTH < DEPTH_MAX:
            traced = trace_ray(rayO, rayD)
            if not traced:
                break
            obj, M, N, col_ray = traced
            # Reflection: create a new ray.
            rayO, rayD = M + \
                N * .0001, normalize(rayD - 2 * np.dot(rayD, N) * N)
            DEPTH += 1
            col += REFLECTION * col_ray
            REFLECTION *= obj.get('reflection', 1.)
        img[IMAGE_HEIGHT - j - 1, i, :] = np.clip(col, 0, 1)

plt.imsave('fig.png', img)
