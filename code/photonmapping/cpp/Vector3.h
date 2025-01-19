#ifndef VECTOR3_H
#define VECTOR3_H

#include <cmath>

class Vector3 {
public:
    double x, y, z;
    
    Vector3(double x_=0, double y_=0, double z_=0): x(x_), y(y_), z(z_) {}
    
    Vector3 operator + (const Vector3& v) const { return Vector3(x+v.x, y+v.y, z+v.z); }
    Vector3 operator - (const Vector3& v) const { return Vector3(x-v.x, y-v.y, z-v.z); }
    Vector3 operator * (double scalar) const { return Vector3(x*scalar, y*scalar, z*scalar); }
    Vector3 operator / (double scalar) const { return Vector3(x/scalar, y/scalar, z/scalar); }
    Vector3 operator - () const { return Vector3(-x, -y, -z); }
    Vector3 operator * (const Vector3& v) const { return Vector3(x*v.x, y*v.y, z*v.z); }
    double dot(const Vector3& v) const { return x*v.x + y*v.y + z*v.z; }
    double norm() const { return std::sqrt(x*x + y*y + z*z); }
    Vector3 normalize() const { double n = norm(); return Vector3(x/n, y/n, z/n); }
};

#endif // VECTOR3_H