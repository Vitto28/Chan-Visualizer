from geometry import Point, angle
from typing import List, Dict, Any, Tuple

steps: List[Dict[str, Any]] = []
record_steps = False

def record_initial_line(_stack: List[Point], sentinel: Point, p: Point):
    if not record_steps:
        return
    steps.append({
        "phase": "start",
        "stack": _stack[:],
        "current": p,
        "sentinel": sentinel,
        "description": "Selected initial point + sentinel"
    })
    return

def record_candidate_test(pivot: Point, pivot_pred: Point, candidate: Point, _stack: List[Point], current_best: Point = None):
    if not record_steps:
        return
    steps.append({
        "phase": "candidate_test",
        "stack": _stack[:],
        "pivot": pivot,
        "pivot_pred": pivot_pred,
        "candidate": candidate,
        "current_best": current_best,
        "description": f"Testing candidate {candidate}"
    })
    return

def record_new_best_candidate(pivot: Point, pivot_pred: Point, new_best: Point, _stack: List[Point]):
    if not record_steps:
        return
    steps.append({
        "phase": "new_best",
        "pivot": pivot,
        "pivot_pred": pivot_pred,
        "new_best": new_best,
        "stack": _stack[:],
        "description": f"New best candidate is {new_best}"
    })
    return

def record_current_hull(_stack: List[Point]):
    if not record_steps:
        return
    steps.append({
        "phase": "current_hull",
        "stack": _stack[:],
        "description": f"Added point { _stack[-1] } to hull (hull size is now {len(_stack)})"
    })
    return

def record_finished(_stack: List[Point]):
    if not record_steps:
        return
    steps.append({
        "phase": "finished",
        "stack": _stack[:],
        "description": "Finished computing hull"
    })
    return

def jarvis_march(points: List[Point], _record_steps: bool = False) -> Tuple[List[Point], List[Dict[str, Any]]]:
    # if dup_x_coord_set(points):
    #     raise ValueError("Input points must have unique x-coordinates.")
    
    global record_steps
    record_steps = _record_steps

    if len(points) < 3:
        return points, steps
    
    hull = []
    
    # identify a point guaranteed to be on the hull (smallest y-coord, use x-coord to break ties)
    v1 = min(points, key=lambda p: (p[1], p[0]))
    hull.append(v1)
    v0 = (v1[0] - 1, v1[1]) # a point directly to the left of the pivot

    record_initial_line(hull, v0, v1)

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

            record_candidate_test(pivot, pivot_pred, p, hull, vi)

            if _angle < min_angle:
                min_angle = _angle
                vi = p
                record_new_best_candidate(pivot, pivot_pred, p, hull)


        assert vi is not None, "There should always be a valid next point since we have at least 3 points and no duplicates."
        if vi == v1: # we've wrapped around to the start
            record_finished(hull)
            break
        hull.append(vi)
        record_current_hull(hull)
        pivot_pred, pivot = hull[-2], hull[-1]

    return hull, steps