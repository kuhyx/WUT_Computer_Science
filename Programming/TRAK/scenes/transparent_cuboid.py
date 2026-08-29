"""A rotated block of green glass standing on a checkered floor.

The floor is deliberately close and low-repeat, so the refraction through the
block is easy to compare against the undistorted tiles beside it.
"""

from sightpy import Cuboid, Glossy, Plane, Refractive, Scene, image, rgb, vec3


def setup_scene(
    width: int = 400, height: int = 300, environment: str = "stormydays.png"
) -> Scene:
    """Build the glass-cuboid scene at `width` x `height` over `environment`."""
    floor = Glossy(
        diff_color=image("checkered_floor.png", repeat=2.0),
        roughness=0.2,
        spec_coeff=0.3,
        diff_coeff=0.7,
        n=vec3(2.2, 2.2, 2.2),
    )  # n = index of refraction
    green_glass = Refractive(n=vec3(1.5 + 4e-8j, 1.5 + 0.0j, 1.5 + 4e-8j))

    scene = Scene()
    scene.add_Camera(
        look_from=vec3(0.0, 0.25, 1.0),
        look_at=vec3(0.0, 0.25, -3.0),
        screen_width=width,
        screen_height=height,
    )

    scene.add_DirectionalLight(Ldir=vec3(0.0, 0.5, 0.5), color=rgb(0.5, 0.5, 0.5))

    scene.add(
        Plane(
            material=floor,
            center=vec3(0, -0.5, -3.0),
            width=6.0,
            height=6.0,
            u_axis=vec3(1.0, 0, 0),
            v_axis=vec3(0, 0, -1.0),
            max_ray_depth=5,
        )
    )

    cb = Cuboid(
        material=green_glass,
        center=vec3(0.00, 0.0001, -0.8),
        width=0.9,
        height=1.0,
        length=0.4,
        shadow=False,
        max_ray_depth=5,
    )
    cb.rotate(θ=30, u=vec3(0, 1, 0))
    scene.add(cb)

    # see sightpy/backgrounds
    scene.add_Background(environment)

    return scene
