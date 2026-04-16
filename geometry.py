import math
from typing import Tuple, List

Point = Tuple[int, int]

def angle(p: Point, q: Point, r: Point) -> float:
    """Returns the angle formed by the ordered triplet (p, q, r) in radians."""
    x1, y1 = p
    x2, y2 = q
    x3, y3 = r

    # vectors pq and qr
    v1x, v1y = x2 - x1, y2 - y1
    v2x, v2y = x3 - x2, y3 - y2

    # calculate the angle using the dot product formula
    dot_product = v1x * v2x + v1y * v2y
    mag_v1 = math.sqrt(v1x**2 + v1y**2)
    mag_v2 = math.sqrt(v2x**2 + v2y**2)

    if mag_v1 == 0 or mag_v2 == 0:
        raise ValueError("Angle is undefined for zero-length vectors.")

    cos_theta = dot_product / (mag_v1 * mag_v2)
    # clamp cos_theta to the range [-1, 1] to avoid numerical issues with acos
    cos_theta = max(-1.0, min(1.0, cos_theta))
    
    return math.acos(cos_theta)

def orientation_test(p: Point, q: Point, r: Point) -> int:
    """Returns the orientation of the ordered triplet (p, q, r).
    0 -> p, q and r are collinear
    1 -> if counter-clockwise (left turn)
    -1 -> if clockwise (right turn)
    """

    x1, y1 = p
    x2, y2 = q
    x3, y3 = r
    det = (y2 - y1) * (x3 - x2) - (x2 - x1) * (y3 - y2)
    if det > 0:
        return 1  # Counter-clockwise
    elif det < 0:
        return -1  # Clockwise
    else:
        return 0  # Collinear
    

def left_tangent_point(hull: List[Point], q: Point) -> int:
    """Finds the index of the left tangent point from the given point q to the convex hull by using binary search."""
    n = len(hull)
    if n == 0:
        return -1
    if n == 1:
        return 0
    low, high = 0, n - 1
    while low <= high:
        mid = (low + high) // 2
        next_index = (mid + 1) % n
        prev_index = (mid - 1 + n) % n

        p = hull[mid]
        p_next = hull[next_index]
        p_prev = hull[prev_index]

        if orientation_test(q, p, p_next) >= 0 and orientation_test(q, p, p_prev) >= 0:
            return mid
        elif orientation_test(q, p, p_prev) < 0:
            # p_prev lies on the wrong side
            high = mid - 1
        else:
            # p_next lies on the wrong side
            low = mid + 1
    return low

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
    for i in range(n):
        for j in range(i + 1, n):
            if dup_x_coord(points[i], points[j]):
                return False
            if check_y and dup_y_coord(points[i], points[j]):
                return False
            for k in range(j + 1, n):
                if are_collinear(points[i], points[j], points[k]):
                    return False
    return True 