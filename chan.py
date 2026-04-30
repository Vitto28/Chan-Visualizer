from geometry import Point, angle, get_tangent_points
from typing import List, Dict, Any, Tuple
from math import ceil



from graham import graham_scan

steps: List[Dict[str, Any]] = []
record_steps = False

def record_mini_hulls(mini_hulls: List[List[Point]]):
    if not record_steps:
        return
    steps.append({
        "phase": "mini_hulls",
        "mini_hulls": [mh[:] for mh in mini_hulls],
        "description": f"Computed {len(mini_hulls)} mini-hulls"
    })
    return

def record_tangent_points(pivot: Point, pivot_pred: Point, tangent_points: List[Point], mini_hulls: List[List[Point]], hull: List[Point]):
    if not record_steps:
        return
    steps.append({
        "phase": "tangent_points",
        "pivot": pivot,
        "pivot_pred": pivot_pred,
        "tangent_points": tangent_points[:],
        "mini_hulls": [mh[:] for mh in mini_hulls],
        "hull": hull[:],
        "description": f"Found tangent points {tangent_points} from pivot {pivot} to each mini-hull"
    })
    return

def record_pivots(pivot: Point, pivot_pred: Point, mini_hulls: List[List[Point]]):
    if not record_steps:
        return
    steps.append({
        "phase": "pivots",
        "pivot": pivot,
        "pivot_pred": pivot_pred,
        "mini_hulls": [mh[:] for mh in mini_hulls],
        "description": f"Selected initial pivot {pivot} and pivot predecessor {pivot_pred}"
    })
    return

def record_candidate_test(pivot: Point, pivot_pred: Point, candidate: Point, mini_hulls: List[List[Point]], hull: List[Point], angle: float, current_best: Point = None):
    if not record_steps:
        return
    steps.append({
        "phase": "candidate_test",
        "pivot": pivot,
        "pivot_pred": pivot_pred,
        "candidate": candidate,
        "current_best": current_best,
        "mini_hulls": [mh[:] for mh in mini_hulls],
        "hull": hull[:],
        "description": f"Testing candidate {candidate} with angle {angle} against current best {current_best}"
    })
    return

def record_new_best_candidate(pivot: Point, pivot_pred: Point, new_best: Point, mini_hulls: List[List[Point]], hull: List[Point]):
    if not record_steps:
        return
    steps.append({
        "phase": "new_best",
        "pivot": pivot,
        "pivot_pred": pivot_pred,
        "new_best": new_best,
        "mini_hulls": [mh[:] for mh in mini_hulls],
        "hull": hull[:],
        "description": f"New best candidate is {new_best}"
    })
    return

def record_current_hull(hull: List[Point], mini_hulls: List[List[Point]]):
    if not record_steps:
        return
    steps.append({
        "phase": "current_hull",
        "hull": hull[:],
        "mini_hulls": [mh[:] for mh in mini_hulls],
        "description": f"Added point {hull[-1]} to hull (hull size is now {len(hull)})"
    })
    return

def record_finished(hull: List[Point], h_star: int):
    if not record_steps:
        return
    steps.append({
        "phase": "finished",
        "hull": hull[:],
        "description": f"Finished computing convex hull with {len(hull)} points using Chan's algorithm with h* = {h_star}"
    })
    return

def record_failure(prev_h_star: int, new_h_star: int):
    if not record_steps:
        return
    steps.append({
        "phase": "failure",
        "prev_h_star": prev_h_star,
        "new_h_star": new_h_star,
        "description": f"Failed with h* = {prev_h_star}, now trying with h* = {new_h_star}"
    })
    return

def graham_aux(points: List[Point]) -> List[Point]:
    """Helper function that computes the convex hull of a subset of points using Graham's scan. This is used as a subroutine in Chan's algorithm. It only returns the hull points without recording steps, since we don't need to visualize the mini-hulls."""
    return graham_scan(points)[0]


def chans_algo(points: List[Point], _record_steps: bool = False) -> Tuple[List[Point], List[Dict[str, Any]]]:

    global record_steps
    record_steps = _record_steps

    if len(points) < 3:
        return points, steps

    pts = points[:]
    n = len(pts)
    hull = []
    h_star = 2 # final hull size guess
    success = False
    while not success:
        h_star = min(h_star**2, n) # TODO: try other growth rates for h_star
        success, hull = conditional_hull(pts, h_star)
        if not success:
            record_failure(h_star // 2, h_star)

    record_finished(hull, h_star)

    return hull, steps


# def conditional_hull(points: List[Point], h: int) -> (bool, List[Point]):
def conditional_hull(points: List[Point], h: int) -> Tuple[bool, List[Point]]:
    k = ceil(len(points) // h) # number of mini-hulls
    # compute the mini-hulls using GS
    mini_hulls = []
    pts = points[:]
    for i in range(k):
        mini_hulls.append(graham_aux(pts[i*h:(i+1)*h]))
    if k * h < len(points):
        mini_hulls.append(graham_aux(pts[k*h:])) # handle the last mini-hull if n is not a multiple of h

    tmp_hull = []

    record_mini_hulls(mini_hulls)

    # mini hack: if k = 1, then we can just return the single mini-hull as the final hull (since it must be the case that h >= |hull|, so the single mini-hull must contain the entire hull)
    if k == 1:
        # print("little hack")
        # TODO: chan only produces the correct hull if we enter this condition :/
        # record_finished(mini_hulls[0], h)
        return True, mini_hulls[0]
    
    # identify a point guaranteed to be on the hull (smallest y-coord, use x-coord to break ties)
    v1 = min(points, key=lambda p: (p[1], p[0]))
    tmp_hull.append(v1)
    v0 = (v1[0] - 1, v1[1]) # a point directly to the left of the pivot

    pivot = v1
    pivot_pred = v0

    record_pivots(pivot, pivot_pred, mini_hulls)

    # while True:
    for _ in range(h):
        # find the left tangent point from vi-1 to each mini-hull
        tangent_points = []
        for mh in mini_hulls:
            # we remove the current pivot from the mini-hull before finding the tangent point, since the pivot is guaranteed to be on the hull and we don't want to accidentally find a tangent point that is actually the pivot itself
            mh_sans_pivot = [p for p in mh if p != pivot]
            pa, pb = get_tangent_points(mh_sans_pivot, pivot)
            # select the one that forms the smaller angle with the pivot and pivot_pred as the tangent point
            tp = pa
            if angle(pivot_pred, pivot, mh_sans_pivot[pb]) < angle(pivot_pred, pivot, mh_sans_pivot[pa]):
                tp = pb
            tangent_points.append(mh_sans_pivot[tp])



            # tangent_index = left_tangent_point(mh_sans_pivot, pivot)
            # tangent_index = left_tangent_point(mh, pivot)
            # print index
            # print(f"Left tangent index for mini-hull {mh} is {tangent_index}")
            # TODO: the tangent_index can not match the returned index of tangent_idx < pivot_idx?
            # tangent_points.append(mh[tangent_index])
        # print(f"Tangent points: {tangent_points}")
        # assert we have as many tangent points as mini-hulls
        assert len(tangent_points) == len(mini_hulls), f"Expected {len(mini_hulls)} tangent points, but got {len(tangent_points)}"
        # print the number of tangent points we have
        print(f"Number of tangent points: {len(tangent_points)}")

        record_tangent_points(pivot, pivot_pred, tangent_points, mini_hulls, tmp_hull)

        vi = None # current best candidate for the next hull point
        min_angle = float('inf')
        # for p in points:
        for p in tangent_points:
            if p == pivot or p == pivot_pred:
                continue
            _angle = angle(pivot_pred, pivot, p)

            record_candidate_test(pivot, pivot_pred, p, mini_hulls, tmp_hull, _angle, vi)

            if _angle < min_angle:
                min_angle = _angle
                vi = p
                record_new_best_candidate(pivot, pivot_pred, p, mini_hulls, tmp_hull)

        assert vi is not None
        if vi == v1: # we've wrapped around to the start
            # TODO: see why this fails
            # print("Its a wrap folks")
            # record_finished(tmp_hull, h)
            return True, tmp_hull
        tmp_hull.append(vi)
        record_current_hull(tmp_hull, mini_hulls)
        pivot_pred, pivot = tmp_hull[-2], tmp_hull[-1]

    # if we reach this point, it means we exceeded the hull size guess, so we need to try again with a larger h
    return False, []
