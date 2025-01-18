#include <iostream>
#include <vector>
#include <cmath>
#include <limits>
#include <random>
#include <fstream>

// Define basic vector operations
class Vector3 {
public:
    double x, y, z;
    
    Vector3(double x_=0, double y_=0, double z_=0): x(x_), y(y_), z(z_) {}
    
    Vector3 operator + (const Vector3& v) const { return Vector3(x+v.x, y+v.y, z+v.z); }
    Vector3 operator - (const Vector3& v) const { return Vector3(x-v.x, y-v.y, z-v.z); }
    Vector3 operator * (double scalar) const { return Vector3(x*scalar, y*scalar, z*scalar); }
    Vector3 operator / (double scalar) const { return Vector3(x/scalar, y/scalar, z/scalar); } // Added operator/
    Vector3 operator - () const { return Vector3(-x, -y, -z); } // Added unary minus operator
    Vector3 operator * (const Vector3& v) const { return Vector3(x*v.x, y*v.y, z*v.z); } // Component-wise multiplication
    double dot(const Vector3& v) const { return x*v.x + y*v.y + z*v.z; }
    double norm() const { return std::sqrt(x*x + y*y + z*z); }
    Vector3 normalize() const { double n = norm(); return Vector3(x/n, y/n, z/n); }
};

typedef Vector3 Color; // Alias for RGB color

// Define the photon
struct Photon {
    Vector3 position;
    Vector3 direction;
    Color power;
    
    Photon(const Vector3& pos, const Vector3& dir, const Color& pow)
        : position(pos), direction(dir), power(pow) {}
};

// Define a simple sphere
class Sphere {
public:
    Vector3 center;
    double radius;
    Color color;
    
    Sphere(const Vector3& c, double r, const Color& col)
        : center(c), radius(r), color(col) {}
    
    bool intersect(const Vector3& ray_origin, const Vector3& ray_direction, double& t, Vector3& hit_point, Vector3& normal) const {
        // Solve quadratic equation for intersection
        Vector3 oc = ray_origin - center;
        double a = ray_direction.dot(ray_direction);
        double b = 2.0 * oc.dot(ray_direction);
        double c = oc.dot(oc) - radius * radius;
        double discriminant = b*b - 4*a*c;
        if (discriminant < 0) {
            return false; // No intersection
        } else {
            double sqrt_discriminant = std::sqrt(discriminant);
            double t0 = (-b - sqrt_discriminant) / (2.0 * a);
            double t1 = (-b + sqrt_discriminant) / (2.0 * a);
            t = (t0 < t1 && t0 > 1e-4) ? t0 : t1;
            if (t < 1e-4) {
                return false;
            }
            hit_point = ray_origin + ray_direction * t;
            normal = (hit_point - center).normalize();
            return true;
        }
    }
};

// Define a simple plane
class Plane {
public:
    Vector3 point;   // A point on the plane
    Vector3 normal;  // Normal to the plane
    Color color;
    
    Plane(const Vector3& p, const Vector3& n, const Color& col)
        : point(p), normal(n.normalize()), color(col) {}
    
    bool intersect(const Vector3& ray_origin, const Vector3& ray_direction, double& t, Vector3& hit_point, Vector3& hit_normal) const {
        double denom = normal.dot(ray_direction);
        if (std::abs(denom) > 1e-6) {
            t = (point - ray_origin).dot(normal) / denom;
            if (t >= 1e-4) {
                hit_point = ray_origin + ray_direction * t;
                hit_normal = normal;
                return true;
            }
        }
        return false;
    }
};

// Random number generators
std::mt19937 rng;
std::uniform_real_distribution<double> uni_dist(0.0, 1.0);

// Random unit vector in a sphere
Vector3 random_unit_vector() {
    double theta = 2 * M_PI * uni_dist(rng);
    double z = 2 * uni_dist(rng) - 1;
    double r = std::sqrt(1 - z*z);
    return Vector3(r * std::cos(theta), r * std::sin(theta), z);
}

// Random direction in hemisphere around normal
Vector3 random_hemisphere_direction(const Vector3& normal) {
    Vector3 dir = random_unit_vector();
    if (dir.dot(normal) < 0) {
        dir = dir * -1;
    }
    return dir;
}

// Global variables
std::vector<Photon> photon_map;
std::vector<void*> objects;  // Pointers to objects
std::vector<int> object_types; // 0 for Sphere, 1 for Plane

// Scene setup
Sphere sphere(Vector3(0, 0, -5), 1.0, Color(1, 0, 0));         // Red sphere
Plane plane(Vector3(0, -1, 0), Vector3(0, 1, 0), Color(0.5, 0.5, 0.5)); // Gray plane

// Light source
Vector3 light_position(-5, 5, -5);
Color light_power(1000.0, 1000.0, 1000.0);  // Intense white light, will scale in code

// Parameters
int num_photons = 10000;   // Number of photons to emit
int max_depth = 5;         // Maximum number of bounces
double gather_radius = 0.5; // Radius for radiance estimation

// Functions
void emit_photons();
void trace_photon(Photon photon, int depth);
Color trace_ray(const Vector3& ray_origin, const Vector3& ray_direction);
Color compute_direct_light(const Vector3& point, const Vector3& normal);
Color estimate_radiance(const Vector3& point, const Vector3& normal);

// Main execution
int main() {
    // Seed random number generator
    rng.seed(std::random_device()());
    
    std::cout << "Emitting photons..." << std::endl;
    // Add objects to the scene
    objects.push_back(&sphere); object_types.push_back(0);
    objects.push_back(&plane);  object_types.push_back(1);
    
    emit_photons();
    std::cout << "Photons stored in photon map: " << photon_map.size() << std::endl;
    
    std::cout << "Rendering image..." << std::endl;
    int width = 200;
    int height = 100;
    std::vector<Color> image(width * height);
    
    double aspect_ratio = double(width) / height;
    double fov = M_PI / 3.0;  // 60 degrees field of view
    
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            // Convert pixel coordinate to camera ray
            double px = (2 * (x + 0.5) / double(width) - 1) * tan(fov / 2.0) * aspect_ratio;
            double py = (1 - 2 * (y + 0.5) / double(height)) * tan(fov / 2.0);
            Vector3 ray_origin(0, 0, 0);
            Vector3 ray_direction = Vector3(px, py, -1).normalize();
            Color color = trace_ray(ray_origin, ray_direction);
            image[y * width + x] = Color(
                std::min(color.x, 1.0),
                std::min(color.y, 1.0),
                std::min(color.z, 1.0)
            );
        }
    }
    
    // Save image to PPM file
    std::ofstream ofs("render.ppm");
    ofs << "P3\n" << width << " " << height << "\n255\n";
    double gamma = 1.0 / 2.2; // Corrected gamma division
    for (const auto& pixel : image) {
        int r = static_cast<int>(std::pow(pixel.x, gamma) * 255);
        int g = static_cast<int>(std::pow(pixel.y, gamma) * 255);
        int b = static_cast<int>(std::pow(pixel.z, gamma) * 255);
        // Clamp values between 0 and 255
        r = std::max(0, std::min(255, r));
        g = std::max(0, std::min(255, g));
        b = std::max(0, std::min(255, b));
        ofs << r << " " << g << " " << b << "\n";
    }
    ofs.close();
    std::cout << "Image saved to render.ppm" << std::endl;
    return 0;
}

void emit_photons() {
    Color per_photon_power = light_power / num_photons; // Scale light power per photon
    for (int i = 0; i < num_photons; ++i) {
        // Emit photons in random directions from the light source
        Vector3 direction = random_unit_vector();
        Photon photon(light_position, direction, per_photon_power);
        trace_photon(photon, 0);
    }
}

void trace_photon(Photon photon, int depth) {
    if (depth > max_depth) {
        return;
    }
    double closest_t = std::numeric_limits<double>::infinity();
    void* hit_object = nullptr;
    int hit_type = -1;
    Vector3 hit_point, normal;
    // Find the nearest intersection
    for (size_t i = 0; i < objects.size(); ++i) {
        double t;
        Vector3 temp_hit_point, temp_normal;
        bool hit = false;
        if (object_types[i] == 0) {
            Sphere* obj = static_cast<Sphere*>(objects[i]);
            hit = obj->intersect(photon.position, photon.direction, t, temp_hit_point, temp_normal);
        } else if (object_types[i] == 1) {
            Plane* obj = static_cast<Plane*>(objects[i]);
            hit = obj->intersect(photon.position, photon.direction, t, temp_hit_point, temp_normal);
        }
        if (hit && t < closest_t) {
            closest_t = t;
            hit_object = objects[i];
            hit_type = object_types[i];
            hit_point = temp_hit_point;
            normal = temp_normal;
        }
    }
    if (hit_object) {
        photon_map.push_back(Photon(hit_point, photon.direction, photon.power));
        // Diffuse reflection
        Vector3 new_direction = random_hemisphere_direction(normal);
        photon.position = hit_point;
        photon.direction = new_direction;
        // Absorb some power
        photon.power = photon.power * 0.8; // Simple absorption
        trace_photon(photon, depth + 1);
    }
}

Color trace_ray(const Vector3& ray_origin, const Vector3& ray_direction) {
    double closest_t = std::numeric_limits<double>::infinity();
    void* hit_object = nullptr;
    int hit_type = -1;
    Vector3 hit_point, normal;
    Color obj_color;
    // Find the nearest intersection
    for (size_t i = 0; i < objects.size(); ++i) {
        double t;
        Vector3 temp_hit_point, temp_normal;
        bool hit = false;
        if (object_types[i] == 0) {
            Sphere* obj = static_cast<Sphere*>(objects[i]);
            hit = obj->intersect(ray_origin, ray_direction, t, temp_hit_point, temp_normal);
            if (hit) obj_color = obj->color;
        } else if (object_types[i] == 1) {
            Plane* obj = static_cast<Plane*>(objects[i]);
            hit = obj->intersect(ray_origin, ray_direction, t, temp_hit_point, temp_normal);
            if (hit) obj_color = obj->color;
        }
        if (hit && t < closest_t) {
            closest_t = t;
            hit_object = objects[i];
            hit_type = object_types[i];
            hit_point = temp_hit_point;
            normal = temp_normal;
        }
    }
    if (hit_object) {
        Color direct_light = compute_direct_light(hit_point, normal);
        Color indirect_light = estimate_radiance(hit_point, normal);
        return obj_color * (direct_light + indirect_light); // Component-wise multiplication
    } else {
        return Color(0, 0, 0); // Background color
    }
}

Color compute_direct_light(const Vector3& point, const Vector3& normal) {
    // Simple Lambertian reflection from light source
    Vector3 direction_to_light = (light_position - point).normalize();
    // Shadow ray
    Vector3 shadow_origin = point + normal * 1e-5;
    Vector3 shadow_ray = direction_to_light;
    bool in_shadow = false;
    for (size_t i = 0; i < objects.size(); ++i) {
        double t;
        Vector3 temp_hit_point, temp_normal;
        bool hit = false;
        if (object_types[i] == 0) {
            Sphere* obj = static_cast<Sphere*>(objects[i]);
            hit = obj->intersect(shadow_origin, shadow_ray, t, temp_hit_point, temp_normal);
        } else if (object_types[i] == 1) {
            Plane* obj = static_cast<Plane*>(objects[i]);
            hit = obj->intersect(shadow_origin, shadow_ray, t, temp_hit_point, temp_normal);
        }
        if (hit) {
            in_shadow = true;
            break;
        }
    }
    if (in_shadow) {
        return Color(0, 0, 0);
    } else {
        double intensity = std::max(0.0, normal.dot(direction_to_light));
        double distance2 = (light_position - point).dot(light_position - point);
        return (light_power * intensity) / (4 * M_PI * distance2);
    }
}

Color estimate_radiance(const Vector3& point, const Vector3& normal) {
    // Gather photons within the gather_radius
    Color accumulated_power(0.0, 0.0, 0.0);
    for (const auto& photon : photon_map) {
        double distance = (photon.position - point).norm();
        if (distance < gather_radius) {
            double weight = std::max(0.0, normal.dot((-photon.direction).normalize()));
            accumulated_power = accumulated_power + photon.power * weight;
        }
    }
    double area = M_PI * gather_radius * gather_radius;
    return accumulated_power / area; // Removed division by num_photons
}