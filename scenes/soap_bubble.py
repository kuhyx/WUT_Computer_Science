from sightpy import *

# define materials to use
def setup_scene(width=400, height=300, environment="lake.png"):
    # Set Scene

    Sc = Scene(ambient_color=rgb(0.01, 0.01, 0.01))

    angle = -np.pi * 0.5
    Sc.add_Camera(screen_height=height, screen_width=width,
                  look_from=vec3(4.0 * np.sin(angle), 0.00, 4.0 * np.cos(angle)),
                  look_at=vec3(0., 0.05, 0.0))

    soap_bubble = ThinFilmInterference(thickness=330, noise=60.)
    Sc.add(Sphere(material=soap_bubble, center=vec3(1., 0.0, 1.5), radius=1.7, shadow=False, max_ray_depth=5))

    Sc.add_Background(environment, blur=10.)

    return Sc
