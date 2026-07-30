"""
Main script to generate a 3D Abaqus model containing randomly
oriented, non-overlapping cuboids inside a box.
"""

import sys
import os
import inspect

# Setup paths for Abaqus script imports
current_frame = inspect.currentframe()
script_path = inspect.getfile(current_frame)
BASE_DIR = os.path.dirname(os.path.abspath(script_path))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Import project modules
from generate_cuboids import generate_cuboids
from generate_model import generate_model
from parameters import config

# Generate random cuboids inside the box
cuboid_data = generate_cuboids(config=config)

# Build the Abaqus model with cuboid holes
generate_model(config=config, cuboid_data=cuboid_data)

print("Main script finished successfully.")
