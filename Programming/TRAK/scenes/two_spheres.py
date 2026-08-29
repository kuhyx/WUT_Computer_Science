"""Two metal spheres -- gold and bluish -- on a checkered floor.

Both use the Glossy material, so this is the scene where the complex index of
refraction and the roughness parameter are easiest to read off the render.
"""

import numpy as np
from sightpy import Glossy, Plane, Scene, Sphere, image, rgb, vec3


def setup_scene(
    width: int = 400, height: int = 300, environment: str = "stormydays.png"
) -> Scene:
    """Build the two-sphere scene at `width` x `height` over `environment`."""
    gold_metal = Glossy(
        diff_color=rgb(1.0, 0.572, 0.184),
        n=vec3(0.15 + 3.58j, 0.4 + 2.37j, 1.54 + 1.91j),
        roughness=0.0,
        spec_coeff=0.2,
        diff_coeff=0.8,
    )  # n = index of refraction
    bluish_metal = Glossy(
        diff_color=rgb(0.0, 0, 0.1),
        n=vec3(1.3 + 1.91j, 1.3 + 1.91j, 1.4 + 2.91j),
        roughness=0.2,
        spec_coeff=0.5,
        diff_coeff=0.3,
    )

    floor = Glossy(
        diff_color=image("checkered_floor.png", repeat=80.0),
        n=vec3(1.2 + 0.3j, 1.2 + 0.3j, 1.1 + 0.3j),
        roughness=0.2,
        spec_coeff=0.3,
        diff_coeff=0.9,
    )

    # Set Scene
    scene = Scene(ambient_color=rgb(0.05, 0.05, 0.05))

    angle = -np.pi / 2 * 0.3
    scene.add_Camera(
        look_from=vec3(2.5 * np.sin(angle), 0.25, 2.5 * np.cos(angle) - 1.5),
        look_at=vec3(0.0, 0.25, -3.0),
        screen_width=width,
        screen_height=height,
    )

    scene.add_DirectionalLight(Ldir=vec3(0.52, 0.45, -0.5), color=rgb(0.15, 0.15, 0.15))

    scene.add(
        Sphere(
            material=gold_metal,
            center=vec3(-0.75, 0.1, -3.0),
            radius=0.6,
            max_ray_depth=3,
        )
    )
    scene.add(
        Sphere(
            material=bluish_metal,
            center=vec3(1.25, 0.1, -3.0),
            radius=0.6,
            max_ray_depth=3,
        )
    )

    scene.add(
        Plane(
            material=floor,
            center=vec3(0, -0.5, -3.0),
            width=120.0,
            height=120.0,
            u_axis=vec3(1.0, 0, 0),
            v_axis=vec3(0, 0, -1.0),
            max_ray_depth=3,
        )
    )

    # see sightpy/backgrounds
    scene.add_Background(environment)

    return scene
