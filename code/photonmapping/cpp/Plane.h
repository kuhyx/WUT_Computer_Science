#ifndef PLANE_H 

class Plane {
public:
    Vector3 point;   // A point on the plane
    Vector3 normal;  // Normal to the plane
    Vector3 color;
    
    Plane(const Vector3& p, const Vector3& n, const Vector3& col)
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


#endif 