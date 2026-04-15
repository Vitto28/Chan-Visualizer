import math
from typing import Tuple, List

Point = Tuple[float, float]

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