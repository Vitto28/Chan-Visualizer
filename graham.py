from geometry import Point, orientation_test, dup_x_coord_set
from typing import List

def graham_scan(points: List[Point]) -> List[Point]:
    if dup_x_coord_set(points):
        raise ValueError("Input points must have unique x-coordinates.")
    
    n = len(points)
    if n < 3:
        return points
    
    # 1. Sort points by x-coordinate
    points.sort(key=lambda p: (p[0], p[1]))

    # 2. Push p1 and p2 onto the stack
    stack = []
    stack.append(points[0])
    stack.append(points[1])

    for i in range(2, n):
        p = points[i]
        pj = stack[-1]
        pj1 = stack[-2]
        while len(stack) > 1 and orientation_test(p, pj, pj1) <= 0:
            stack.pop()
        stack.append(p)
    
    return stack