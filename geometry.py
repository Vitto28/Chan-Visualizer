import math
import numpy as np
from typing import Tuple, List

import itertools

Point = Tuple[int, int]

def angle(p: Point, q: Point, r: Point) -> float:
    """Returns the signed angle formed by the ordered triplet (p, q, r).
    Positive values indicate a counter-clockwise turn, and negative values indicate a clockwise turn.
    """
    # Vectors from q to p and q to r
    px, py = p
    qx, qy = q
    rx, ry = r
    v1 = (qx - px, qy - py)
    v2 = (rx - qx, ry - qy)

    # Cross product (z-component) gives the signed sine of the angle
    cross = v1[0] * v2[1] - v1[1] * v2[0]
    # Dot product gives the cosine component
    dot = v1[0] * v2[0] + v1[1] * v2[1]

    return math.atan2(cross, dot)
    
def turn(p: Point, q: Point, r: Point) -> float:
    x1, y1 = p
    x2, y2 = q
    x3, y3 = r
    # matrix is 3 by 3, first column is all 1s
    mat = np.array([
        [1, x1, y1],
        [1, x2, y2],
        [1, x3, y3],
    ])
    det = np.linalg.det(mat)
    return det

def orientation_test(p: Point, q: Point, r: Point) -> int:
    """Returns the orientation of the ordered triplet (p, q, r).
    0 -> p, q and r are collinear
    1 -> if counter-clockwise (left turn)
    -1 -> if clockwise (right turn)
    """

    # x1, y1 = p
    # x2, y2 = q
    # x3, y3 = r
    # # matrix is 3 by 3, first column is all 1s
    # mat = np.array([
    #     [1, x1, y1],
    #     [1, x2, y2],
    #     [1, x3, y3],
    # ])
    # det = np.linalg.det(mat)
    # # det = angle(p, q, r)  # we can use the angle function since it gives us the same information about the turn direction, and also gives us the angle magnitude which we can use for tie-breaking in Chan's algorithm
    det = turn(p, q, r)
    if det > 0:
        return 1  # Counter-clockwise
    elif det < 0:
        return -1  # Clockwise
    else:
        return 0  # Collinear
    

def left_tangent_point(hull: List[Point], q: Point) -> Point:
    """Finds the left tangent point from the given point q to the convex hull by using binary search."""
    print(f" === Finding left tangent point from {q} to hull with points: {hull} === ")
    idx = 0; # index of the left tangent point
    n = len(hull)
    assert n > 0, "Hull must have at least one point to find a tangent"
    low, high = 0, n - 1
    while low <= high:
        mid = low + (high - low) // 2
        next_index = (mid + 1) % n
        prev_index = (mid - 1 + n) % n

        p = hull[mid]
        p_next = hull[next_index]
        p_prev = hull[prev_index]
            
        # print these three
        print(f"Testing hull point p: {p} with prev: {p_prev} and next: {p_next} against query point q: {q}")

        if orientation_test(q, p, p_next) > 0 and orientation_test(q, p, p_prev) > 0:
            idx = mid
            break
        elif orientation_test(q, p, p_prev) < 0:
            # p_prev lies on the wrong side, choose the left interval
            high = mid - 1
        else:
            # p_next lies on the wrong side, choose the right interval
            low = mid + 1
    idx = low + (high - low) // 2
    return hull[idx]


# === Degeneracy checks ===
def are_collinear(p: Point, q: Point, r: Point) -> bool:
    """Check if points p, q, r are collinear."""
    return orientation_test(p, q, r) == 0

def dup_x_coord(p: Point, q: Point) -> bool:
    """Check if points p and q have the same x-coordinate."""
    return p[0] == q[0]

def dup_x_coord_set(points: List[Point]) -> bool:
    """Check if there are at least two points with the same x-coordinate."""
    seen_x = set()
    for p in points:
        if p[0] in seen_x:
            return True
        seen_x.add(p[0])
    return False

def dup_y_coord(p: Point, q: Point) -> bool:
    """Check if points p and q have the same y-coordinate."""
    return p[1] == q[1]

def dup_y_coord_set(points: List[Point]) -> bool:
    """Check if there are at least two points with the same y-coordinate."""
    seen_y = set()
    for p in points:
        if p[1] in seen_y:
            return True
        seen_y.add(p[1])
    return False

def general_position(points: List[Point], check_y=False) -> bool:
    """Check if the points are in general position (no three collinear, no duplicate x-coords, and optionally no duplicate y-coords)."""
    n = len(points)
    # the gen random pts function already ensures that there are no duplicate points, so we only need to check for collinearity 
    groups = itertools.combinations(points, 3)
    for p, q, r in groups:
        print(f"Checking points {p}, {q}, {r} for collinearity...")
        if are_collinear(p, q, r):
            print(f"Points {p}, {q}, {r} are collinear.")
            return False
    return True 