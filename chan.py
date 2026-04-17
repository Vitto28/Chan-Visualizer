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
    k = ceil(len(points) // h) # number of mini-hulls
    # compute the mini-hulls using GS
    mini_hulls = []
    pts = points[:]
    for i in range(k):
        mini_hulls.append(graham_scan(pts[i*h:(i+1)*h]))
    if k * h < len(points):
        mini_hulls.append(graham_scan(pts[k*h:])) # handle the last mini-hull if n is not a multiple of h

    final_hull = []

    # mini hack: if k = 1, then we can just return the single mini-hull as the final hull (since it must be the case that h >= |hull|, so the single mini-hull must contain the entire hull)
    if k == 1:
        print("little hack")
        return True, mini_hulls[0]
    
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
        print(f"Tangent points: {tangent_points}")

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

        # # plot the mini-hulls, tangent points, and current hull
        # import matplotlib.pyplot as plt
        # plt.figure(figsize=(10, 8))
        # xs, ys = zip(*points)
        # plt.scatter(xs, ys, color='blue', label='Random Points')
        # for mh in mini_hulls:
        #     mh_xs, mh_ys = zip(*mh)
        #     plt.plot(mh_xs + (mh_xs[0],), mh_ys + (mh_ys[0],), color='orange', label='Mini Hull')
        # tangent_xs, tangent_ys = zip(*tangent_points)
        # plt.scatter(tangent_xs, tangent_ys, color='green', label='Tangent Points', s=100)
        # hull_xs, hull_ys = zip(*final_hull)
        # plt.scatter([pivot[0]], [pivot[1]], color='red', label='Current Pivot')
        # plt.plot(hull_xs + (hull_xs[0],), hull_ys + (hull_ys[0],), color='red', label='Current Hull')
        # plt.title(f'Chan\'s Algorithm with h* = {h}')
        # plt.xlabel('X-axis')
        # plt.ylabel('Y-axis')
        # plt.legend()
        # plt.grid()
        # plt.show()

        assert vi is not None
        if vi == v1: # we've wrapped around to the start
            print("Its a wrap folks")
            return True, final_hull
        final_hull.append(vi)
        pivot_pred, pivot = final_hull[-2], final_hull[-1]

    # if we reach this point, it means we exceeded the hull size guess, so we need to try again with a larger h
    return False, []
