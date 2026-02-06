import numpy as np
import matplotlib.pyplot as plt
import time

PHOTONS = 0

# Define basic vector operations
class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def __add__(self, other):
        return Vector3(self.x+other.x, self.y+other.y, self.z+other.z)
    
    def __sub__(self, other):
        return Vector3(self.x-other.x, self.y-other.y, self.z-other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x*scalar, self.y*scalar, self.z*scalar)
    
    def dot(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z
    
    def norm(self):
        return np.sqrt(self.dot(self))
    
    def normalize(self):
        n = self.norm()
        return Vector3(self.x/n, self.y/n, self.z/n)

# Define the photon
class Photon:
    def __init__(self, position, direction, power):
        self.position = position
        self.direction = direction
        self.power = power

# Define a simple sphere
class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

    def intersect(self, ray_origin, ray_direction):
        # Solve quadratic equation for intersection
        oc = ray_origin - self.center
        a = ray_direction.dot(ray_direction)
        b = 2.0 * oc.dot(ray_direction)
        c = oc.dot(oc) - self.radius*self.radius
        discriminant = b*b - 4*a*c
        if discriminant < 0:
            return None  # No intersection
        else:
            t = (-b - np.sqrt(discriminant)) / (2.0*a)
            if t < 0:
                t = (-b + np.sqrt(discriminant)) / (2.0*a)
            if t < 0:
                return None
            hit_point = ray_origin + ray_direction * t
            normal = (hit_point - self.center).normalize()
            return (t, hit_point, normal)
        
# Define a simple plane
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

# Scene setup
sphere = Sphere(Vector3(0, 0, -5), 1.0, np.array([1, 0, 0]))  # Red sphere
plane = Plane(Vector3(0, -1, 0), Vector3(0, 1, 0), np.array([0.5, 0.5, 0.5]))  # Gray plane

objects = [sphere, plane]

# Light source
light_position = Vector3(-5, 5, -5)
light_power = np.array([1, 1, 1]) * 1000  # Intense white light

# Photon map
photon_map = []

# Parameters
num_photons = 10000  # Number of photons to emit
max_depth = 5  # Maximum number of bounces
gather_radius = 0.5  # Radius for radiance estimation

def emit_photons():
    for _ in range(num_photons):
        # Emit photons in random directions from the light source
        direction = random_unit_vector()
        power = light_power / num_photons
        photon = Photon(light_position, direction, power)
        trace_photon(photon, 0)

def trace_photon(photon, depth):
    global PHOTONS
    PHOTONS += 1
    if depth > max_depth:
        return
    closest_t = np.inf
    hit_object = None
    hit_info = None
    # Find the nearest intersection
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
        # Diffuse reflection
        new_direction = random_hemisphere_direction(normal)
        photon.position = hit_point
        photon.direction = new_direction
        # Absorb some power
        photon.power = photon.power * 0.8  # Simple absorption
        trace_photon(photon, depth+1)

def random_unit_vector():
    theta = np.random.uniform(0, 2*np.pi)
    z = np.random.uniform(-1, 1)
    r = np.sqrt(1 - z*z)
    return Vector3(r * np.cos(theta), r * np.sin(theta), z)

def random_hemisphere_direction(normal):
    dir = random_unit_vector()
    if dir.dot(normal) < 0:
        dir = Vector3(-dir.x, -dir.y, -dir.z)
    return dir

def render_image(width, height):
    aspect_ratio = width / height
    fov = np.pi / 3  # 60 degrees field of view
    image = np.zeros((height, width, 3))
    for y in range(height):
        for x in range(width):
            # Convert pixel coordinate to camera ray
            px = (2 * (x + 0.5) / width - 1) * np.tan(fov / 2) * aspect_ratio
            py = (1 - 2 * (y + 0.5) / height) * np.tan(fov / 2)
            ray_origin = Vector3(0, 0, 0)
            ray_direction = Vector3(px, py, -1).normalize()
            color = trace_ray(ray_origin, ray_direction)
            image[y, x, :] = np.clip(color, 0, 1)
    return image

def trace_ray(ray_origin, ray_direction):
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
                hit_info = (hit_point, normal, obj.color)
    if hit_object:
        hit_point, normal, color = hit_info
        direct_light = compute_direct_light(hit_point, normal)
        indirect_light = estimate_radiance(hit_point, normal)
        return color * (direct_light + indirect_light)
    else:
        return np.array([0, 0, 0])  # Background color

def compute_direct_light(point, normal):
    # Simple Lambertian reflection from light source
    direction_to_light = (light_position - point).normalize()
    # Shadow ray
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
        return intensity * light_power / (4 * np.pi * (light_position - point).norm()**2)

def estimate_radiance(point, normal):
    # Gather photons within the gather_radius
    accumulated_power = np.array([0.0, 0.0, 0.0])
    for photon_pos, photon_power in photon_map:
        distance = (photon_pos - point).norm()
        if distance < gather_radius:
            weight = max(0, normal.dot((photon_pos - point).normalize()))
            accumulated_power += photon_power * weight
    area = np.pi * gather_radius ** 2
    return accumulated_power / (area * num_photons)

# Main execution
if __name__ == '__main__':
    print("Emitting photons...")
    emit_photons()
    
    print("Rendering image...")
    width = 100
    height = 100
    t0 = time.time()
    image = render_image(width, height)
    
    print (f"Render Took: {round(time.time() - t0, 2)}s\n"
        f"resolution: {width}x{height}\n"
        f"photons (emitted): {num_photons}\n"
        f"photons (reflected): {PHOTONS - num_photons}\n"
        f"photons (total): {PHOTONS}\n"
        f"rays: {width*height}"
        )
    
    # Display the image
    plt.imshow(image)
    plt.axis('off')
    plt.show()
