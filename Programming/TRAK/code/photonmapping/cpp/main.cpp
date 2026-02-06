#include <iostream>
#include <vector>
#include <cmath>
#include <limits>
#include <random>
#include <fstream>
#include <fstream>
#include <chrono>
#include "Vector3.h"
#include "Sphere.h"
#include "Plane.h"


// Define the photon
struct Photon {
    Vector3 position;
    Vector3 direction;
    Vector3 power;
    
    Photon(const Vector3& pos, const Vector3& dir, const Vector3& pow)
        : position(pos), direction(dir), power(pow) {}
};

// Define a simple plane

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
int ray_number = 0;
int photon_number = 0;


// Scene setup
Sphere sphere(Vector3(0, 0, -5), 1.0, Vector3(1, 0, 0));         // Red sphere
Plane plane(Vector3(0, -1, 0), Vector3(0, 1, 0), Vector3(0.5, 0.5, 0.5)); // Gray plane
// Light source
Vector3 light_position(-5, 5, -5);
Vector3 light_power(1000.0, 1000.0, 1000.0);  // Intense white light, will scale in code


// Functions
void emit_photons(const int num_photons, const int max_depth);
void trace_photon(Photon photon, int depth, const int max_depth);
Vector3 trace_ray(const Vector3& ray_origin, const Vector3& ray_direction, const double gather_radius);
Vector3 compute_direct_light(const Vector3& point, const Vector3& normal);
Vector3 estimate_radiance(const Vector3& point, const Vector3& normal, const double gather_radius);

// Main execution
int main(int argc, char* argv[]) {
    auto start = std::chrono::high_resolution_clock::now(); // Start timer
    int num_photons = 10000;
    int max_depth = 5;
    double gather_radius = 0.5;

    if (argc > 1) {
        num_photons = std::atoi(argv[1]);
        if (num_photons <= 0) {
            std::cerr << "Invalid number of photons. Using default: 10000" << std::endl;
            num_photons = 10000;
        }
    }
    if (argc > 2) {
        max_depth = std::atoi(argv[2]);
        if (max_depth < 0) {
            std::cerr << "Invalid max_depth. Using default: 5" << std::endl;
            max_depth = 5;
        }
    }
    if (argc > 3) {
        gather_radius = std::atof(argv[3]);
        if (gather_radius <= 0) {
            std::cerr << "Invalid gather_radius. Using default: 0.5" << std::endl;
            gather_radius = 0.5;
        }
    }
    std::cout << "Number of photons: " << num_photons << std::endl;
    std::cout << "Max depth: " << max_depth << std::endl;
    std::cout << "Gather radius: " << gather_radius << std::endl;

    // Seed random number generator
    rng.seed(std::random_device()());
    
    std::cout << "Emitting photons..." << std::endl;
    // Add objects to the scene
    objects.push_back(&sphere); object_types.push_back(0);
    objects.push_back(&plane);  object_types.push_back(1);
    
    emit_photons(num_photons, max_depth);
    const int photons_in_map = photon_map.size();
    
    std::cout << "Rendering image..." << std::endl;
    int width = 200;
    int height = 100;
    std::vector<Vector3> image(width * height);
    
    double aspect_ratio = double(width) / height;
    double fov = M_PI / 3.0;  // 60 degrees field of view
    
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {    
            // Convert pixel coordinate to camera ray
            double px = (2 * (x + 0.5) / double(width) - 1) * tan(fov / 2.0) * aspect_ratio;
            double py = (1 - 2 * (y + 0.5) / double(height)) * tan(fov / 2.0);
            Vector3 ray_origin(0, 0, 0);
            Vector3 ray_direction = Vector3(px, py, -1).normalize();
            Vector3 color = trace_ray(ray_origin, ray_direction, gather_radius);
            image[y * width + x] = Vector3(
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
    std::cout << "Image generated" << std::endl; 
    std::cout << "width: " << width << std::endl;
    std::cout << "height: " << width << std::endl;
    std::cout << "photons in map: " << photons_in_map << std::endl;
    std::cout << "count of photons: " << photon_number << std::endl;
    std::cout << "count of rays: " << ray_number << std::endl;
    std::cout << "Image saved to render.ppm" << std::endl;
    std::chrono::duration<double> elapsed = std::chrono::high_resolution_clock::now() - start;
    std::cout << "Execution time: " << elapsed.count() << " seconds" << std::endl;
    return 0;
}

void emit_photons(const int num_photons, const int max_depth) {
    Vector3 per_photon_power = light_power / num_photons; // Scale light power per photon
    for (int i = 0; i < num_photons; ++i) {
        Vector3 direction = random_unit_vector();
        Photon photon(light_position, direction, per_photon_power);
        trace_photon(photon, 0, max_depth);
    }
}

void trace_photon(Photon photon, int depth, const int max_depth) {
    photon_number++;
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
        trace_photon(photon, depth + 1, max_depth);
    }
}

Vector3 trace_ray(const Vector3& ray_origin, const Vector3& ray_direction, const double gather_radius) {
    ray_number++;
    double closest_t = std::numeric_limits<double>::infinity();
    void* hit_object = nullptr;
    int hit_type = -1;
    Vector3 hit_point, normal;
    Vector3 obj_color;
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
        Vector3 direct_light = compute_direct_light(hit_point, normal);
        Vector3 indirect_light = estimate_radiance(hit_point, normal, gather_radius);
        return obj_color * (direct_light + indirect_light); // Component-wise multiplication
    } else {
        return Vector3(0, 0, 0); // Background color
    }
}

Vector3 compute_direct_light(const Vector3& point, const Vector3& normal) {
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
        return Vector3(0, 0, 0);
    } else {
        double intensity = std::max(0.0, normal.dot(direction_to_light));
        double distance2 = (light_position - point).dot(light_position - point);
        return (light_power * intensity) / (4 * M_PI * distance2);
    }
}

Vector3 estimate_radiance(const Vector3& point, const Vector3& normal, const double gather_radius) {
    // Gather photons within the gather_radius
    Vector3 accumulated_power(0.0, 0.0, 0.0);
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