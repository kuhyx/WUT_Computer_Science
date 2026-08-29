#!/usr/bin/env python3
"""Lab 6 driver: run another script in this directory by path.

`script_path` was filled in by hand during the lab, which is why it is empty
here -- the file is kept as submitted.
"""

import runpy

script_path = ""  # path to script
runpy.run_path(script_path, run_name="__main__")
