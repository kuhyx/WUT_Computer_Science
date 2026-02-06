#ifndef SPHERE_H
#define SPHERE_H

#include "Vector3.h"

class Sphere {
public:
    Vector3 center;
    double radius;
    Vector3 color;
    
    Sphere(const Vector3& c, double r, const Vector3& col)
        : center(c), radius(r), color(col) {}
    
    bool intersect(const Vector3& ray_origin, const Vector3& ray_direction, double& t, Vector3& hit_point, Vector3& normal) const {
        Vector3 oc = ray_origin - center;
        double a = ray_direction.dot(ray_direction);
        double b = 2.0 * oc.dot(ray_direction);
        double c = oc.dot(oc) - radius * radius;
        double discriminant = b * b - 4 * a * c;
        if (discriminant > 0) {
            t = (-b - std::sqrt(discriminant)) / (2.0 * a);
            hit_point = ray_origin + ray_direction * t;
            normal = (hit_point - center).normalize();
            return true;
        }
        return false;
    }
};

#endif // SPHERE_H