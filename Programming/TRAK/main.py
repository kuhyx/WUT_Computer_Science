#!/usr/bin/env python3
"""Entry point: render a scene with one of the three algorithms in this course.

The algorithm, scene, resolution and output path all default to `config.ini`
and are overridable on the command line.
"""

import argparse
import importlib
import logging
from pathlib import Path

import matplotlib.pyplot as plt
from photon_mapping import render_photon_mapping
from rendering import ray_trace
from utils import load_config, parse_resolution

logger = logging.getLogger(__name__)


def main() -> None:
    """Parse the command line over `config.ini` defaults and run the renderer."""
    # default config
    config = load_config("config.ini")

    # Parse
    parser = argparse.ArgumentParser(description="Rendering Program")
    parser.add_argument(
        "--algorithm",
        type=str,
        help="Algorithm to use",
        default=config.get("DEFAULT", "algorithm"),
    )
    parser.add_argument(
        "--scene",
        type=str,
        help="Name of the scene to render (without .py).",
        default=config.get("DEFAULT", "scene"),
    )
    parser.add_argument(
        "--environment",
        type=str,
        help="Environment file",
        default=config.get("DEFAULT", "environment"),
    )
    parser.add_argument(
        "--env_blur",
        type=str,
        help="Environment blur",
        default=config.get("DEFAULT", "env_blur"),
    )
    parser.add_argument(
        "--resolution",
        type=str,
        help="Image resolution (WIDTHxHEIGHT)",
        default=config.get("DEFAULT", "resolution"),
    )
    parser.add_argument(
        "--samples_per_pixel",
        type=int,
        default=config.get("ray_tracing", "samples_per_pixel"),
        help="Samples per pixel for rendering.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=config.get("DEFAULT", "output"),
        help="Output file name.",
    )

    parser.add_argument(
        "--num_spheres",
        type=int,
        default=3,
        help="Number of spheres in the scene for Ray Tracing 0",
    )
    parser.add_argument(
        "--num_photons",
        type=int,
        default=config.getint("photon_mapping", "num_photons"),
        help="Number of photons for photon mapping",
    )
    parser.add_argument(
        "--max_depth",
        type=int,
        default=config.getint("photon_mapping", "max_depth"),
        help="Maximum depth for photon tracing",
    )
    parser.add_argument(
        "--gather_radius",
        type=float,
        default=config.getfloat("photon_mapping", "gather_radius"),
        help="Radius for radiance estimation in photon mapping",
    )
    # The render is always written to outputs/; this only controls whether a
    # viewer is ALSO popped up. It defaults off because img.show() shells out
    # to xdg-open and then blocks until a human closes the window -- which
    # left ../../run.sh run Programming/TRAK hanging for 45 minutes after the
    # ray trace had actually finished.
    parser.add_argument(
        "--show",
        action="store_true",
        help="also open the finished image in a viewer (blocks until closed)",
    )

    args = parser.parse_args()

    width, height = parse_resolution(args.resolution)

    # Run the selected algorithm
    if args.algorithm == "ray_tracing0":
        logger.info("Starting ray tracing zero...")
        ray_trace(
            args.num_spheres,
            args.environment,
            image_width=width,
            # na razie generujemy w kodzie, ale potem trzeba będzie obj wczytywać
            image_height=height,
            output_file=Path("outputs") / args.output,
        )
    elif args.algorithm == "ray_tracing":
        logger.info("Starting ray tracing...")
        try:
            logger.info("%s", args.scene)
            scene_module = importlib.import_module(f"scenes.{args.scene}")
        except ModuleNotFoundError:
            logger.info(
                "Error: Scene '%s' not found in the 'scenes' directory.", args.scene
            )
            return
        try:
            scene = scene_module.setup_scene(
                width=width, height=height, environment=f"{args.environment}"
            )
        except AttributeError:
            logger.info(
                "Error: Scene '%s' does not define a `setup_scene` function.",
                args.scene,
            )
            return
        # Renderowanie
        logger.info(
            "Rendering scene '%s' with %s samples per pixel...",
            args.scene,
            args.samples_per_pixel,
        )
        img = scene.render(samples_per_pixel=args.samples_per_pixel)
        output_path = Path("outputs") / args.output
        img.save(output_path)
        logger.info("Image saved to %s", output_path)
        if args.show:
            img.show()
    elif args.algorithm == "photon_mapping":
        logger.info("Starting photon mapping...")
        image = render_photon_mapping(
            width, height, args.num_photons, args.max_depth, args.gather_radius
        )
        plt.imshow(image)
        plt.axis("off")
        output_path = Path("outputs") / args.output
        plt.savefig(output_path)
        logger.info("Image saved to %s", output_path)
        if args.show:
            plt.show()
    else:
        logger.info("Unknown algorithm: %s", args.algorithm)
        return


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    main()
