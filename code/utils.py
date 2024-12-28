from configparser import ConfigParser

def load_config(config_path):
    config = ConfigParser()
    config.read(config_path)
    return config

def parse_resolution(resolution):
    try:
        width, height = map(int, resolution.lower().split('x'))
        return width, height
    except ValueError:
        raise ValueError("Resolution must be in the format WIDTHxHEIGHT, e.g., 1920x1080.")