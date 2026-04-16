from geometry import Point, orientation_test, dup_x_coord_set
from typing import List

def graham_scan(points: List[Point]) -> List[Point]:
    if dup_x_coord_set(points):
        raise ValueError("Input points must have unique x-coordinates.")
    
    if len(points) < 3:
        return points
    
    pts = points[:]
    pts.sort(key=lambda p: (p[0], p[1]))

    upper_chain = compute_chain(pts)
    lower_chain = compute_chain(pts[::-1])

    # remove the last point of each chain to avoid duplication of the start/end points
    upper_chain.pop()
    lower_chain.pop()

    return upper_chain + lower_chain


def compute_chain(points: List[Point]) -> List[Point]:
    """Computes either the upper or lower chain of the convex hull, depending on the order of the input points."""
    n = len(points)
    # create a local copy of the points to avoid modifying the original list
    pts = points[:]
    stack = []
    stack.append(pts[0])
    stack.append(pts[1])
    for i in range(2, n):
        p = pts[i]
        pj = stack[-1]
        pj1 = stack[-2]
        while len(stack) > 1 and orientation_test(p, pj, pj1) <= 0:
            stack.pop()
            if len(stack) > 1:
                pj = stack[-1]
                pj1 = stack[-2]
        stack.append(p)
    return stack