# import random
import numpy as np
import matplotlib.pyplot as plt

from geometry import general_position

from benchmark import random_small_hull, generate_random_points

from graham import graham_scan
from jarvis import jarvis_march
from chan import chans_algo

from visualizer import visualize

def main():
    n = 10
    # x_max = 10000
    # y_max = 10000
    x_max, y_max = n * 10, n * 10 # scale max coordinates with n to reduce the chance of duplicates and to make the plots look nicer
    pts = generate_random_points(n, x_max, y_max)
    # pts = random_small_hull(n, x_max, y_max)
    print(f"Generated {len(pts)} random points.")

    # fig = plt.figure(figsize=(10, 8))
    xs, ys = zip(*pts)
    # plt.scatter(xs, ys, color='blue', label='Random Points')
    # plt.title('Random Points')
    # plt.xlabel('X-axis')
    # plt.ylabel('Y-axis')
    # plt.legend()
    # plt.grid()
    # plt.show()

    # run the three algorithms on the same set of points and verify that they all produce the same hull (up to cyclic shifts and reversals)
    # algos = {
    #     "Graham's Scan": graham_scan(pts[:]),
    #     "Jarvis March": jarvis_march(pts[:]),
    #     "Chan's Algorithm": chans_algo(pts[:])
    # }

    gs_hull, gs_steps = graham_scan(pts[:], _record_steps=True)
    # print len of steps
    print(f"Graham's Scan produced a hull with {len(gs_hull)} points and recorded {len(gs_steps)} steps.")
    visualize(pts, gs_steps, "graham_scan")

    # plot the final hull as a sanity check
    hull_xs, hull_ys = zip(*gs_hull)
    plt.figure(figsize=(10, 8))
    plt.scatter(xs, ys, color='blue', label='Random Points')
    plt.plot(hull_xs + (hull_xs[0],), hull_ys + (hull_ys[0],), color='red', label='Convex Hull')
    plt.title(f"Graham's Scan Final Hull (size: {len(gs_hull)})")
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid()
    plt.show()


    # assert the three algorithms produced the same hull (up to cyclic shifts and reversals)
    # hulls = list(algos.values())
    # gs_hull = hulls[0]
    # for algo_name, hull in algos.items():
    #     if len(hull) != len(gs_hull):
    #         raise ValueError(f"{algo_name} produced a hull of size {len(hull)}, which is different from the size of the hull produced by Graham's Scan ({len(gs_hull)}).")
    #     if set(hull) != set(gs_hull):
    #         raise ValueError(f"{algo_name} produced a different set of hull points than Graham's Scan.")
    # print(f"All three algorithms produced the same hull with {len(gs_hull)} points: {gs_hull}")

    # print(f"Convex Hull has {len(hull)} points: {hull}")

    # plot the hulls produced by each of the three algorithms, side by side for easy comparison
    # fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    # for ax, (algo_name, hull) in zip(axs, algos.items()):
    #     ax.scatter(xs, ys, color='blue', label='Random Points')
    #     hull_xs, hull_ys = zip(*hull)
    #     ax.plot(hull_xs + (hull_xs[0],), hull_ys + (hull_ys[0],), color='red', label='Convex Hull')
    #     ax.set_title(f"{algo_name} (Hull size: {len(hull)})")
    #     ax.set_xlabel('X-axis')
    #     ax.set_ylabel('Y-axis')
    #     ax.legend()
    #     ax.grid()
    # plt.tight_layout()
    # plt.show()

if __name__ == "__main__":
    main()