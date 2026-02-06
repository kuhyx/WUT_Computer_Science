import numpy as np
import matplotlib.pyplot as plt

# Define basic vector operations
class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def norm(self):
        return np.sqrt(self.dot(self))

    def normalize(self):
        n = self.norm()
        return Vector3(self.x / n, self.y / n, self.z / n)


class Photon:
    def __init__(self, position, direction, power):
        self.position = position
        self.direction = direction
        self.power = power


class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

    def intersect(self, ray_origin, ray_direction):
        oc = ray_origin - self.center
        a = ray_direction.dot(ray_direction)
        b = 2.0 * oc.dot(ray_direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return None
        else:
            t = (-b - np.sqrt(discriminant)) / (2.0 * a)
            if t < 0:
                t = (-b + np.sqrt(discriminant)) / (2.0 * a)
            if t < 0:
                return None
            hit_point = ray_origin + ray_direction * t
            normal = (hit_point - self.center).normalize()
            return (t, hit_point, normal)


class Plane:
    def __init__(self, point, normal, color):
        self.point = point
        self.normal = normal.normalize()
        self.color = color

    def intersect(self, ray_origin, ray_direction):
        denom = self.normal.dot(ray_direction)
        if abs(denom) > 1e-6:
            t = (self.point - ray_origin).dot(self.normal) / denom
            if t >= 0:
                hit_point = ray_origin + ray_direction * t
                return (t, hit_point, self.normal)
        return None


def render_photon_mapping(width, height, num_photons, max_depth, gather_radius):
    # Photon mapping logic
    photon_map = []
    sphere = Sphere(Vector3(0, 0, -5), 1.0, np.array([1, 0, 0]))  # Red sphere
    plane = Plane(Vector3(0, -1, 0), Vector3(0, 1, 0), np.array([0.5, 0.5, 0.5]))  # Gray plane
    objects = [sphere, plane]

    light_position = Vector3(-5, 5, -5)
    light_power = np.array([1, 1, 1]) * 1000

    def emit_photons():
        for _ in range(num_photons):
            direction = random_unit_vector()
            power = light_power / num_photons
            photon = Photon(light_position, direction, power)
            trace_photon(photon, 0)

    def trace_photon(photon, depth):
        if depth > max_depth:
            return
        closest_t = np.inf
        hit_object = None
        hit_info = None
        for obj in objects:
            result = obj.intersect(photon.position, photon.direction)
            if result:
                t, hit_point, normal = result
                if t < closest_t:
                    closest_t = t
                    hit_object = obj
                    hit_info = (hit_point, normal)
        if hit_object:
            hit_point, normal = hit_info
            photon_map.append((hit_point, photon.power))
            new_direction = random_hemisphere_direction(normal)
            photon.position = hit_point
            photon.direction = new_direction
            photon.power = photon.power * 0.8
            trace_photon(photon, depth + 1)

    def random_unit_vector():
        theta = np.random.uniform(0, 2 * np.pi)
        z = np.random.uniform(-1, 1)
        r = np.sqrt(1 - z * z)
        return Vector3(r * np.cos(theta), r * np.sin(theta), z)

    def random_hemisphere_direction(normal):
        dir = random_unit_vector()
        if dir.dot(normal) < 0:
            dir = Vector3(-dir.x, -dir.y, -dir.z)
        return dir

    def trace_ray(ray_origin, ray_direction):
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
                    hit_info = (hit_point, normal, obj.color)
        if hit_object:
            hit_point, normal, color = hit_info
            direct_light = compute_direct_light(hit_point, normal)
            indirect_light = estimate_radiance(hit_point, normal)
            return color * (direct_light + indirect_light)
        else:
            return np.array([0, 0, 0])

    def compute_direct_light(point, normal):
        direction_to_light = (light_position - point).normalize()
        shadow_origin = point + normal * 1e-5
        shadow_ray = direction_to_light
        in_shadow = False
        for obj in objects:
            result = obj.intersect(shadow_origin, shadow_ray)
            if result:
                in_shadow = True
                break
        if in_shadow:
            return np.array([0, 0, 0])
        else:
            intensity = max(0, normal.dot(direction_to_light))
            return intensity * light_power / (4 * np.pi * (light_position - point).norm() ** 2)

    def estimate_radiance(point, normal):
        accumulated_power = np.array([0.0, 0.0, 0.0])
        for photon_pos, photon_power in photon_map:
            distance = (photon_pos - point).norm()
            if distance < gather_radius:
                weight = max(0, normal.dot((photon_pos - point).normalize()))
                accumulated_power += photon_power * weight
        area = np.pi * gather_radius ** 2
        return accumulated_power / area

    emit_photons()

    aspect_ratio = width / height
    fov = np.pi / 3
    image = np.zeros((height, width, 3))
    for y in range(height):
        for x in range(width):
            px = (2 * (x + 0.5) / width - 1) * np.tan(fov / 2) * aspect_ratio
            py = (1 - 2 * (y + 0.5) / height) * np.tan(fov / 2)
            ray_origin = Vector3(0, 0, 0)
            ray_direction = Vector3(px, py, -1).normalize()
            color = trace_ray(ray_origin, ray_direction)
            image[y, x, :] = np.clip(color, 0, 1)

    return image
