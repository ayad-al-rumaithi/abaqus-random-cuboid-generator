import numpy as np

def cuboids_vertices(center, width, height, depth, rotation_matrix):
    """
    Compute the 8 vertices of a cuboid given its center, dimensions, and rotation.

    Parameters:
        center : list or array-like [x, y, z]
            The cuboid's center coordinates.
        width, height, depth : float
            Cuboid dimensions along local X, Y, Z axes.
        rotation_matrix : np.ndarray, shape (3,3)
            Rotation applied to the cuboid (local → global coordinates).

    Returns:
        np.ndarray, shape (8,3)
            Array of 3D coordinates for each cuboid vertex.
    """
    dx, dy, dz = width / 2.0, height / 2.0, depth / 2.0

    # Define vertices in cuboid's local reference frame (centered at origin)
    local_coords = np.array([
        [-dx, -dy, -dz], [ dx, -dy, -dz], [ dx,  dy, -dz], [-dx,  dy, -dz],
        [-dx, -dy,  dz], [ dx, -dy,  dz], [ dx,  dy,  dz], [-dx,  dy,  dz]
    ])

    # Apply rotation
    rotated = (rotation_matrix @ local_coords.T).T
    # Translate to global coordinates
    translated = rotated + np.array(center)

    return translated