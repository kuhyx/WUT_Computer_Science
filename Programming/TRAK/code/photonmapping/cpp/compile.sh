#!/bin/bash
#
# Build the photon-mapping demo.
set -euo pipefail

g++ -O2 main.cpp -o photon_mapping
