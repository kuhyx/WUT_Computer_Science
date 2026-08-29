"""One soap bubble in front of a blurred backdrop.

The colours come from thin-film interference, not from a texture: the shell
is a few hundred nanometres thick, so different wavelengths cancel at
different angles.
"""

import numpy as np
from sightpy import Scene, Sphere, ThinFilmInterference, rgb, vec3


def setup_scene(
    width: int = 400, height: int = 300, environment: str = "lake.png"
) -> Scene:
    """Build the soap-bubble scene at `width` x `height` over `environment`."""
    scene = Scene(ambient_color=rgb(0.01, 0.01, 0.01))

    angle = -np.pi * 0.5
    scene.add_Camera(
        screen_height=height,
        screen_width=width,
        look_from=vec3(4.0 * np.sin(angle), 0.00, 4.0 * np.cos(angle)),
        look_at=vec3(0.0, 0.05, 0.0),
    )

    soap_bubble = ThinFilmInterference(thickness=330, noise=60.0)
    scene.add(
        Sphere(
            material=soap_bubble,
            center=vec3(1.0, 0.0, 1.5),
            radius=1.7,
            shadow=False,
            max_ray_depth=5,
        )
    )

    scene.add_Background(environment, blur=10.0)

    return scene
