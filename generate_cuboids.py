import random
import math
import numpy as np

from rotation_matrix_zxz import rotation_matrix_zxz
from cuboids_vertices import cuboids_vertices
from cuboids_intersection import cuboids_intersection

def generate_cuboids(config):
    """
    Generate non-overlapping, randomly rotated cuboids inside a 3D box.

    Parameters:
        config : dict
            Configuration dictionary containing box/cuboid dimensions,
            count, maximum attempts, random seed, and minimum clearance.

    Returns:
        list of tuples: (center, (alpha, beta, gamma), vertices)
            Center coordinates, ZXZ Euler angles (degrees), and vertex coordinates.
    """
    # Extract parameters from the config dictionary
    BOX_W, BOX_H, BOX_D = config["BOX_DIMS"]
    CUB_W, CUB_H, CUB_D = config["CUBOID_DIMS"]
    num_cuboids = config["NUM_CUBOIDS"]
    max_attempts = config["MAX_ATTEMPTS"]
    random_seed = config["RANDOM_SEED"]
    min_clearance = config["MIN_CLEARANCE"]

    random.seed(random_seed)
    np.random.seed(random_seed)

    cuboid_data = []
    attempts = 0

    while len(cuboid_data) < num_cuboids and attempts < max_attempts:
        attempts += 1

        # Random ZXZ Euler angles
        alpha = random.uniform(0, 360)
        gamma = random.uniform(0, 360)
        # Beta sampled to ensure uniform rotation over sphere
        beta = math.degrees(math.acos(2*random.random() - 1))

        R = rotation_matrix_zxz(alpha, beta, gamma)

        # Random cuboid center inside the box
        center = (
            random.uniform(0, BOX_W),
            random.uniform(0, BOX_H),
            random.uniform(0, BOX_D)
        )

        # Compute rotated vertices
        vertices = cuboids_vertices(center, CUB_W, CUB_H, CUB_D, R)

        # Check if cuboid satisfies clearance with box boundaries
        box_limit = np.array([BOX_W, BOX_H, BOX_D])
        if np.any(vertices.min(axis=0) < min_clearance) or np.any(vertices.max(axis=0) > (box_limit - min_clearance)):
            continue

        # Check intersection and clearance with previously placed cuboids
        if any(cuboids_intersection(vertices, placed, min_clearance) for _, _, placed in cuboid_data):
            continue

        cuboid_data.append((center, (alpha, beta, gamma), vertices))

    print(f"Placed {len(cuboid_data)} cuboids after {attempts} attempts.")
    return cuboid_data
