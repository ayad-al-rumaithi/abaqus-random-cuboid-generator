import math
import numpy as np

def rotation_matrix_zxz(alpha, beta, gamma):
    """
    Compute rotation matrix from extrinsic ZXZ Euler angles (degrees).

    Rotation order:
        1. Rotate around global Z-axis by alpha
        2. Rotate around global X-axis by beta
        3. Rotate around global Z-axis by gamma

    Parameters:
        alpha, beta, gamma : float
            Euler angles in degrees.

    Returns:
        np.ndarray, shape (3,3)
            Rotation matrix corresponding to the given ZXZ angles.
    """
    a, b, g = map(math.radians, [alpha, beta, gamma])

    # First Z rotation
    Rz1 = np.array([[math.cos(a), -math.sin(a), 0],
                    [math.sin(a),  math.cos(a), 0],
                    [0, 0, 1]])

    # X rotation
    Rx  = np.array([[1, 0, 0],
                    [0, math.cos(b), -math.sin(b)],
                    [0, math.sin(b),  math.cos(b)]])

    # Second Z rotation
    Rz2 = np.array([[math.cos(g), -math.sin(g), 0],
                    [math.sin(g),  math.cos(g), 0],
                    [0, 0, 1]])

    # Extrinsic rotation: apply Rz1 → Rx → Rz2
    return Rz2 @ Rx @ Rz1