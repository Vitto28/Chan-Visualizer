from geometry import Point, orientation_test, dup_x_coord_set
from typing import List, Dict, Any, Tuple

steps: List[Dict[str, Any]] = []
# PHASES = ...
record_steps = False

def record_pop(_stack: List[Point], popped: Point, p: Point):
    if not record_steps:
        return
    steps.append({
        "phase": "pop",
        "popped": popped,
        "stack": _stack[:],
        "current": p,
        "description": f"Popped point {popped} from stack"
    })
    return

def record_push(_stack: List[Point], pushed: Point, p: Point):
    if not record_steps:
        return
    steps.append({
        "phase": "push",
        "pushed": pushed,
        "stack": _stack[:],
        "current": p,
        "description": f"Pushed point {pushed} onto stack (stack size is now {len(_stack)})"
    })
    return

def record_finished_chain(_stack: List[Point], chain_type: str):
    if not record_steps:
        return
    steps.append({
        "phase": "finished_chain",
        "stack": _stack[:],
        "description": f"Computed {chain_type} chain"
    })
    return


# def graham_scan(points: List[Point], _record_steps: bool = False) -> List[Point]:
def graham_scan(points: List[Point], _record_steps: bool = False) -> Tuple[List[Point], List[Dict[str, Any]]]:
    # if dup_x_coord_set(points):
        # raise ValueError("Input points must have unique x-coordinates.")

    global record_steps
    record_steps = _record_steps

    if len(points) < 3:
        return points, steps
    
    pts = points[:]
    pts.sort(key=lambda p: (p[0], p[1]))

    upper_chain = compute_chain(pts)
    record_finished_chain(upper_chain, "upper")
    lower_chain = compute_chain(pts[::-1])
    record_finished_chain(lower_chain, "lower")

    # remove the last point of each chain to avoid duplication of the start/end points
    upper_chain.pop()
    lower_chain.pop()

    hull = upper_chain + lower_chain

    # record finished step
    steps.append({
        "phase": "finished",
        "stack": hull[:],
        "description": f"Finished computing convex hull with {len(hull)} points"
    })

    # print the number of steps recorded
    print(f"Graham's Scan recorded {len(steps)} steps.")

    return hull, steps


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
            record_pop(stack, pj, p)
            if len(stack) > 1:
                pj = stack[-1]
                pj1 = stack[-2]
        stack.append(p)
        record_push(stack, p, p)
    return stack