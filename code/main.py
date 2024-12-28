import argparse
from configparser import ConfigParser
from rendering import ray_trace
from utils import load_config, parse_resolution

def main():
    # default config
    config = load_config('config.ini')

    # Parse
    parser = argparse.ArgumentParser(description="Rendering Program")
    parser.add_argument('--algorithm', type=str, help='Algorithm to use', default=config.get('DEFAULT', 'algorithm'))
    parser.add_argument('--scene', type=str, help='Path to scene file', default=config.get('DEFAULT', 'scene'))
    parser.add_argument('--environment_map', type=str, help='Environment map file', default=config.get('DEFAULT', 'environment_map'))
    parser.add_argument('--resolution', type=str, help='Image resolution (WIDTHxHEIGHT)',
                        default=config.get('DEFAULT', 'resolution'))

    parser.add_argument('--num_spheres', type=int, default=3, help='Number of spheres in the scene')

    args = parser.parse_args()

    width, height = parse_resolution(args.resolution)

    # Run the selected algorithm
    if args.algorithm == "ray_tracing":
        print("Starting ray tracing...")
        # ray_trace(args.scene, args.environment_map, image_width=width, image_height=height, output_file="output_ray_traced.png")
        ray_trace(args.num_spheres, args.environment_map, image_width=width, image_height=height, # na razie generujemy w kodzie, ale potem trzeba będzie obj wczytywać
                  output_file="output_ray_traced.png")
    else:
        print(f"Unknown algorithm: {args.algorithm}")
        return

if __name__ == '__main__':
    main()
