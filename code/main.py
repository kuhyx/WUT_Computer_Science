""" Renders an image using raytracing """
import numpy as np
import matplotlib.pyplot as plt

IMAGE_WIDTH = 400
IMAGE_HEIGHT = 300


def normalize(x):
    """
    Normalize a vector.

    Parameters:
    x (numpy.ndarray): The input vector to be normalized.

    Returns:
    numpy.ndarray: The normalized vector.
    """
    x /= np.linalg.norm(x)
    return x


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
    elif object_['type'] == 'sphere':
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
    # Find first point of intersection with the scene.
    t = np.inf
    obj_idx = -1
    for index, object_ in enumerate(scene):
        t_obj = intersect(ray_origin, ray_direction, object_)
        if t_obj < t:
            t, obj_idx = t_obj, index
    # Return None if the ray does not intersect any object.
    if t == np.inf:
        return
    # Find the object.
    object_ = scene[obj_idx]
    # Find the point of intersection on the object.
    intersection_point = ray_origin + ray_direction * t
    # Find properties of the object.
    normal = get_normal(object_, intersection_point)
    color = get_color(object_, intersection_point)
    to_light = normalize(L - intersection_point)
    to_origin = normalize(O - intersection_point)
    # Shadow: find if the point is shadowed or not.
    shadow_intersections = [intersect(  intersection_point + normal * .0001,
                                        to_light,
                                        obj_sh
                                        )
                            for k, obj_sh in enumerate(scene) if k != obj_idx]
    if shadow_intersections and min(shadow_intersections) < np.inf:
        return
    # Start computing the color.
    color_ray = ambient
    # Lambert shading (diffuse).
    diffuse_intensity = object_.get('diffuse_c', diffuse_c) * max(
        np.dot(normal, to_light), 0)
    color_ray += diffuse_intensity * color

    # Blinn-Phong shading (specular).
    half_vector = normalize(to_light + to_origin)
    specular_intensity = object_.get('specular_c', specular_c) * max(
        np.dot(normal, half_vector), 0) ** specular_k
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
    return dict(type='sphere', position=np.array(position),
                radius=np.array(radius), color=np.array(color), reflection=.5)


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
    return dict(type='plane', position=np.array(position),
                normal=np.array(normal),
                color=lambda M: (color_plane0
                                 if (int(M[0] * 2) % 2) == (int(M[2] * 2) % 2)
                                 else color_plane1),
                diffuse_c=.75, specular_c=.5, reflection=.25)


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
ambient = .05
diffuse_c = 1.
specular_c = 1.
specular_k = 50

depth_max = 5  # Maximum number of light reflections.
col = np.zeros(3)  # Current color.
O = np.array([0., 0.35, -1.])  # Camera.
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
        D = normalize(Q - O)
        depth = 0
        rayO, rayD = O, D
        reflection = 1.
        # Loop through initial and secondary rays.
        while depth < depth_max:
            traced = trace_ray(rayO, rayD)
            if not traced:
                break
            obj, M, N, col_ray = traced
            # Reflection: create a new ray.
            rayO, rayD = M + \
                N * .0001, normalize(rayD - 2 * np.dot(rayD, N) * N)
            depth += 1
            col += reflection * col_ray
            reflection *= obj.get('reflection', 1.)
        img[IMAGE_HEIGHT - j - 1, i, :] = np.clip(col, 0, 1)

plt.imsave('fig.png', img)
