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