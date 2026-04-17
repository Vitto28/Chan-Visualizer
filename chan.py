from geometry import Point, angle, left_tangent_point
from typing import List
from math import ceil



from graham import graham_scan


def chans_algo(points: List[Point]) -> List[Point]:

    if len(points) < 3:
        return points

    pts = points[:]
    n = len(pts)
    hull = []
    h_star = 2 # final hull size guess
    success = False
    while not success:
        h_star = min(h_star**2, n) # TODO: try other growth rates for h_star
        print(f"Trying with h* = {h_star}...")
        success, hull = conditional_hull(pts, h_star)
    return hull


def conditional_hull(points: List[Point], h: int) -> (bool, List[Point]):
    k = ceil(len(points) / h) # number of mini-hulls
    # compute the mini-hulls using GS
    mini_hulls = []
    for i in range(k):
        mini_hulls.append(graham_scan(points[i*h:(i+1)*h]))

    final_hull = []
    
    # identify a point guaranteed to be on the hull (smallest y-coord, use x-coord to break ties)
    v1 = min(points, key=lambda p: (p[1], p[0]))
    final_hull.append(v1)
    v0 = (v1[0] - 1, v1[1]) # a point directly to the left of the pivot

    pivot = v1
    pivot_pred = v0
    # while True:
    for _ in range(h):
        # find the left tangent point from vi-1 to each mini-hull
        tangent_points = []
        for mh in mini_hulls:
            tangent_index = left_tangent_point(mh, pivot)
            # print index
            # print(f"Left tangent index for mini-hull {mh} is {tangent_index}")
            tangent_points.append(mh[tangent_index])
        # print(f"Tangent points: {tangent_points}")

        vi = None # current best candidate for the next hull point
        min_angle = float('inf')
        # for p in points:
        for p in tangent_points:
            if p == pivot or p == pivot_pred:
                continue
            _angle = angle(pivot_pred, pivot, p)
            if _angle < min_angle:
                min_angle = _angle
                vi = p

        assert vi is not None
        if vi == v1: # we've wrapped around to the start
            return True, final_hull
        final_hull.append(vi)
        pivot_pred, pivot = final_hull[-2], final_hull[-1]

    # if we reach this point, it means we exceeded the hull size guess, so we need to try again with a larger h
    return False, []

    # v1 = min(points, key=lambda p: (p[1], p[0])) # bottommost point
    # v0 = (v1[0] - 1, v1[1]) # a point directly to the left of the pivot

    # final_hull = [v1]

    # pivot = v1 # v(i-1)
    # pivot_pred = v0 # v(i-2)

    # for _ in range(h):
    #     # find the left tangent point from vi-1 to each mini-hull
    #     tangent_points = []
    #     for mh in mini_hulls:
    #         tangent_index = left_tangent_point(mh, pivot)
    #         tangent_points.append(mh[tangent_index])

    #     # find the point among the tangent points that forms the smallest angle with v0 and v1
    #     vi = None
    #     min_angle = float('inf')
    #     for p in tangent_points:
    #         if p == pivot or p == pivot_pred:
    #             continue
    #         _angle = angle(pivot_pred, pivot, p)
    #         if _angle < min_angle:
    #             min_angle = _angle
    #             vi = p

    #     assert vi is not None
    #     if vi == v1: # we've wrapped around to the start, so we know the hull is complete
    #         return True, final_hull
    #     final_hull.append(vi) # add the most recent vertex
    #     pivot_pred, pivot = final_hull[-2], final_hull[-1]


    # # if we reach this point, it means we exceeded the hull size guess, so we need to try again with a larger h
    # return False, []
