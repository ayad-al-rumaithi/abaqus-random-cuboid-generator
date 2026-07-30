"""
Input parameters for the model.
"""

config = {
    "BOX_DIMS": (60.0, 40.0, 50.0),  # Box dimensions (X, Y, Z)
    "CUBOID_DIMS": (25.0, 15.0, 5.0),  # Cuboid dimensions (length, width, thickness)
    "NUM_CUBOIDS": 6,  # Number of cuboids to place
    "MAX_ATTEMPTS": 100000,  # Maximum random placement attempts
    "RANDOM_SEED": 42,  # Random seed for reproducibility
    "MIN_CLEARANCE": 1.0,  # Minimum distance between cuboids, and between cuboids and box boundaries
}
