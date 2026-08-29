"""The Cornell box: a closed room lit by a ceiling panel.

The reference scene for global illumination -- the colour bleeding from the
red and green walls onto the white ones is the whole point of it.
"""

from sightpy import (
    Cuboid,
    Diffuse,
    Emissive,
    Plane,
    Refractive,
    Scene,
    Sphere,
    rgb,
    vec3,
)


def setup_scene(
    width: int = 400, height: int = 300, environment: str | None = None
) -> Scene:
    """Build the Cornell box at `width` x `height`.

    `environment` is accepted so every scene has one interface, and ignored:
    the box is closed, so no background is ever visible.
    """
    del environment

    scene = Scene(ambient_color=rgb(0.00, 0.00, 0.00))

    scene.add_Camera(
        screen_width=width,
        screen_height=height,
        look_from=vec3(278, 278, 800),
        look_at=vec3(278, 278, 0),
        focal_distance=1.0,
        field_of_view=40,
    )

    # define materials to use

    green_diffuse = Diffuse(diff_color=rgb(0.12, 0.45, 0.15))
    red_diffuse = Diffuse(diff_color=rgb(0.65, 0.05, 0.05))
    white_diffuse = Diffuse(diff_color=rgb(0.73, 0.73, 0.73))
    emissive_white = Emissive(color=rgb(15.0, 15.0, 15.0))
    blue_glass = Refractive(n=vec3(1.5 + 0.05e-8j, 1.5 + 0.02e-8j, 1.5 + 0.0j))

    # this is the light
    scene.add(
        Plane(
            material=emissive_white,
            center=vec3(213 + 130 / 2, 554, -227.0 - 105 / 2),
            width=130.0,
            height=105.0,
            u_axis=vec3(1.0, 0.0, 0),
            v_axis=vec3(0.0, 0, 1.0),
        ),
        importance_sampled=True,
    )

    scene.add(
        Plane(
            material=white_diffuse,
            center=vec3(555 / 2, 555 / 2, -555.0),
            width=555.0,
            height=555.0,
            u_axis=vec3(0.0, 1.0, 0),
            v_axis=vec3(1.0, 0, 0.0),
        )
    )

    scene.add(
        Plane(
            material=green_diffuse,
            center=vec3(-0.0, 555 / 2, -555 / 2),
            width=555.0,
            height=555.0,
            u_axis=vec3(0.0, 1.0, 0),
            v_axis=vec3(0.0, 0, -1.0),
        )
    )

    scene.add(
        Plane(
            material=red_diffuse,
            center=vec3(555.0, 555 / 2, -555 / 2),
            width=555.0,
            height=555.0,
            u_axis=vec3(0.0, 1.0, 0),
            v_axis=vec3(0.0, 0, -1.0),
        )
    )

    scene.add(
        Plane(
            material=white_diffuse,
            center=vec3(555 / 2, 555, -555 / 2),
            width=555.0,
            height=555.0,
            u_axis=vec3(1.0, 0.0, 0),
            v_axis=vec3(0.0, 0, -1.0),
        )
    )

    scene.add(
        Plane(
            material=white_diffuse,
            center=vec3(555 / 2, 0.0, -555 / 2),
            width=555.0,
            height=555.0,
            u_axis=vec3(1.0, 0.0, 0),
            v_axis=vec3(0.0, 0, -1.0),
        )
    )

    cb = Cuboid(
        material=white_diffuse,
        center=vec3(182.5, 165, -285 - 160 / 2),
        width=165,
        height=165 * 2,
        length=165,
        shadow=False,
    )
    cb.rotate(θ=15, u=vec3(0, 1, 0))
    scene.add(cb)

    scene.add(
        Sphere(
            material=blue_glass,
            center=vec3(370.5, 165 / 2, -65 - 185 / 2),
            radius=165 / 2,
            shadow=False,
            max_ray_depth=3,
        ),
        importance_sampled=True,
    )

    return scene
