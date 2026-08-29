#!/usr/bin/env python3
"""Configuration and CLI-argument helpers shared by the renderer entry point."""

from configparser import ConfigParser


def load_config(config_path: str) -> ConfigParser:
    """Read `config_path` and return the parsed configuration.

    A missing file is not an error: ``ConfigParser.read`` ignores it and the
    caller falls back to argparse defaults.
    """
    config = ConfigParser()
    config.read(config_path)
    return config


def parse_resolution(resolution: str) -> tuple[int, int]:
    """Split a ``WIDTHxHEIGHT`` string into its two integer components."""
    try:
        width, height = map(int, resolution.lower().split("x"))
    except ValueError as err:
        msg = "Resolution must be in the format WIDTHxHEIGHT, e.g., 1920x1080."
        raise ValueError(msg) from err
    return width, height
