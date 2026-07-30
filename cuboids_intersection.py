import numpy as np

def cuboids_intersection(vertices1, vertices2, min_clearance, tol=1e-8):
    """
    Determine whether two cuboids violate the minimum clearance distance 
    using the Separating Axis Theorem (SAT).

    Parameters:
        vertices1 : np.ndarray, shape (8,3)
            Coordinates of the first cuboid's vertices.
        vertices2 : np.ndarray, shape (8,3)
            Coordinates of the second cuboid's vertices.
        min_clearance : float
            Minimum acceptable spatial gap between the cuboids.
        tol : float
            Tolerance for ignoring near-zero vectors.

    Returns:
        bool: True if cuboids violate clearance/intersect; 
              False if safely separated by min_clearance.
    """
    # Cuboid axes (edges from the first vertex)
    axes1 = [vertices1[1] - vertices1[0],
             vertices1[3] - vertices1[0],
             vertices1[4] - vertices1[0]]

    axes2 = [vertices2[1] - vertices2[0],
             vertices2[3] - vertices2[0],
             vertices2[4] - vertices2[0]]

    # Combine primary structural axes
    axes = axes1 + axes2

    # Add all cross-product axes between edges of both cuboids
    for a1 in axes1:
        for a2 in axes2:
            axes.append(np.cross(a1, a2))

    # Single, universal loop to check separation and filter out near-zero axes
    for axis in axes:
        norm = np.linalg.norm(axis)
        if norm < tol:
            continue  # safely skip zero vectors / duplicate parallel lines
            
        axis_unit = axis / norm
        proj1 = [np.dot(v, axis_unit) for v in vertices1]
        proj2 = [np.dot(v, axis_unit) for v in vertices2]

        # Calculate the clearance gap along this projection axis
        gap = max(min(proj1) - max(proj2), min(proj2) - max(proj1))

        # If the gap along this axis is greater or equal to min_clearance, 
        # the cuboids safely satisfy the spacing constraint.
        if gap >= min_clearance:
            return False  # safe distance found → no violation

    return True  # Violation or intersection found along all axes
