from geometry import Point, angle
from typing import List, Dict, Any, Tuple

steps: List[Dict[str, Any]] = []
record_steps = False

def jarvis_march(points: List[Point]) -> Tuple[List[Point], List[Dict[str, Any]]]:
    # if dup_x_coord_set(points):
    #     raise ValueError("Input points must have unique x-coordinates.")
    
    if len(points) < 3:
        return points, steps
    
    hull = []
    
    # identify a point guaranteed to be on the hull (smallest y-coord, use x-coord to break ties)
    v1 = min(points, key=lambda p: (p[1], p[0]))
    hull.append(v1)
    v0 = (v1[0] - 1, v1[1]) # a point directly to the left of the pivot

    pivot = v1
    pivot_pred = v0
    while True:
        vi = None # current best candidate for the next hull point
        min_angle = float('inf')
        for p in points:
            if p == pivot or p == pivot_pred:
                continue
            # if vi is None:
            #     vi = p
            #     min_angle = angle(pivot_pred, pivot, p)
            #     continue
            _angle = angle(pivot_pred, pivot, p)
            if _angle < min_angle:
                min_angle = _angle
                vi = p

        assert vi is not None, "There should always be a valid next point since we have at least 3 points and no duplicates."
        if vi == v1: # we've wrapped around to the start
            break
        hull.append(vi)
        pivot_pred, pivot = hull[-2], hull[-1]

    return hull, steps