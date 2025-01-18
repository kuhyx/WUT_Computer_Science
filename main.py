import argparse
from configparser import ConfigParser
from rendering import ray_trace
from utils import load_config, parse_resolution
import importlib
import os
# from scenes.cornell_box import *

def main():
    # default config
    config = load_config('config.ini')

    # Parse
    parser = argparse.ArgumentParser(description="Rendering Program")
    parser.add_argument('--algorithm', type=str, help='Algorithm to use', default=config.get('DEFAULT', 'algorithm'))
    parser.add_argument('--scene', type=str, help='Name of the scene to render (without .py).', default=config.get('DEFAULT', 'scene'))
    parser.add_argument('--environment', type=str, help='Environment file', default=config.get('DEFAULT', 'environment'))
    parser.add_argument('--env_blur', type=str, help='Environment blur', default=config.get('DEFAULT', 'env_blur'))
    parser.add_argument('--resolution', type=str, help='Image resolution (WIDTHxHEIGHT)',
                        default=config.get('DEFAULT', 'resolution'))
    parser.add_argument("--samples_per_pixel", type=int, default=config.get('ray_tracing', 'samples_per_pixel'), help="Samples per pixel for rendering.")
    parser.add_argument("--output", type=str, default=config.get('DEFAULT', 'output'), help="Output file name.")

    parser.add_argument('--num_spheres', type=int, default=3, help='Number of spheres in the scene for Ray Tracing 0')

    args = parser.parse_args()

    width, height = parse_resolution(args.resolution)

    # Run the selected algorithm
    if args.algorithm == "ray_tracing0":
        print("Starting ray tracing zero...")
        # ray_trace(args.scene, args.environment_map, image_width=width, image_height=height, output_file="output_ray_traced.png")
        ray_trace(args.num_spheres, args.environment_map, image_width=width, image_height=height,  # na razie generujemy w kodzie, ale potem trzeba będzie obj wczytywać
                  output_file="output_ray_traced.png")
    elif args.algorithm == "ray_tracing":
        print("Starting ray tracing...")
        try:
            print(args.scene)
            scene_module = importlib.import_module(f"scenes.{args.scene}")
        except ModuleNotFoundError:
            print(f"Error: Scene '{args.scene}' not found in the 'scenes' directory.")
            return
        try:
            scene = scene_module.setup_scene(width=width, height=height, environment=f"{args.environment}")
        except AttributeError:
            print(f"Error: Scene '{args.scene}' does not define a `setup_scene` function.")
            return
        # Renderowanie
        print(f"Rendering scene '{args.scene}' with {args.samples_per_pixel} samples per pixel...")
        img = scene.render(samples_per_pixel=args.samples_per_pixel)
        output_path = os.path.join("outputs", args.output)
        img.save(output_path)
        print(f"Image saved to {output_path}")
        img.show()
    else:
        print(f"Unknown algorithm: {args.algorithm}")
        return

if __name__ == '__main__':
    main()
