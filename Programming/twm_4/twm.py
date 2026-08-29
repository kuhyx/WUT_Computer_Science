#!/usr/bin/env python3
"""Smoke check: report which TensorFlow the notebook will actually run against."""

import sys

import tensorflow as tf

sys.stdout.write(f"{tf.__version__}\n")
