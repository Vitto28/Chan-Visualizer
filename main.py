# import random
import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple, List

from geometry import general_position, Point

from benchmark import random_small_hull, generate_random_points

from graham import graham_scan
from jarvis import jarvis_march
from chan import chans_algo

from visualizer import visualize, RENDERERS

def main():
    n = 2**3
    pts = []
    # # x_max = 10000
    # # y_max = 10000
    x_max, y_max = n * 10, n * 10 # scale max coordinates with n to reduce the chance of duplicates and to make the plots look nicer
    print(f"Generating {n} random points with max coordinates ({x_max}, {y_max})...")
    pts = generate_random_points(n, x_max, y_max)
    # pts = random_small_hull(n, x_max, y_max)
    # print(f"Generated {len(pts)} random points.")

    # assert that the number of points is a power of 2 for better visualization of Chan's algorithm
    assert (n & (n - 1) == 0) and n != 0, f"Number of points n = {n} is not a power of 2, which may lead to less interesting visualizations of Chan's algorithm. Please choose n to be a power of 2 for better visualizations."

    # fig = plt.figure(figsize=(10, 8))
    # xs, ys = zip(*pts)
    # plt.scatter(xs, ys, color='blue', label='Random Points')
    # plt.title('Random Points')
    # plt.xlabel('X-axis')
    # plt.ylabel('Y-axis')
    # plt.legend()
    # plt.grid()
    # plt.show()

    # debugging
    # load point set from a randomly chosen .txt file in the same directory as the script, with the format "x y" per line
    # import os


    # gs_hull, _ = graham_scan(pts[:], _record_steps=False)
    # jm_hull, _ = jarvis_march(pts[:], _record_steps=False)

    # # plot the hulls side by side for visual verification
    # fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    # xs, ys = zip(*pts)
    # axs[0].scatter(xs, ys, color='blue', label='Random Points')
    # gs_xs, gs_ys = zip(*gs_hull)
    # axs[0].plot(gs_xs + (gs_xs[0],), gs_ys + (gs_ys[0],), color='red', label='Graham\'s Scan Hull')
    # # hull points are also plotted as red dots for better visibility
    # axs[0].scatter(gs_xs, gs_ys, color='red', label='Graham\'s Scan Hull Points', s=100, edgecolors='black')
    # axs[0].set_title(f"Graham's Scan (Hull size: {len(gs_hull)})")
    # axs[0].set_xlabel('X-axis')
    # axs[0].set_ylabel('Y-axis')
    # axs[0].legend()
    # axs[0].grid()
    # axs[1].scatter(xs, ys, color='blue', label='Random Points')
    # jm_xs, jm_ys = zip(*jm_hull)
    # axs[1].plot(jm_xs + (jm_xs[0],), jm_ys + (jm_ys[0],), color='green', label='Jarvis March Hull')
    # # hull points are also plotted as green dots for better visibility
    # axs[1].scatter(jm_xs, jm_ys, color='green', label='Jarvis March Hull Points', s=100, edgecolors='black')
    # axs[1].set_title(f"Jarvis March (Hull size: {len(jm_hull)})")
    # axs[1].set_xlabel('X-axis')
    # axs[1].set_ylabel('Y-axis')
    # axs[1].legend()
    # axs[1].grid()
    # plt.tight_layout()
    # plt.show()

    # if set(gs_hull) != set(jm_hull):
    #     raise ValueError(f"Graham's Scan and Jarvis March produced different hulls. GS hull: {gs_hull} with length {len(gs_hull)}, JM hull: {jm_hull} with length {len(jm_hull)}")

    # run the three algorithms on the same set of points and verify that they all produce the same hull (up to cyclic shifts and reversals)
    # take only the hull points, ignore the recorded steps for now
    algos = {
        # "graham_scan": graham_scan(pts[:], _record_steps=True),
        # "jarvis_march": jarvis_march(pts[:], _record_steps=True),
        "chan_algorithm": chans_algo(pts[:], _record_steps=True)
    }

    import time
    def _save_point_set(input_points, trial_num=None):
        timestamp = int(time.time())
        filename = f"saved_points_{timestamp}.txt"
        with open(filename, "w") as f:
            for p in input_points:
                f.write(f"{p[0]} {p[1]}\n")
        print(f"Saved current point set to {filename}")

    running_trials = False

    if running_trials:
        n_trials = 100
        # run GS and JM on n_trials random point sets and verify they produce the same hull
        discrepancy = False
        for i in range(n_trials):
            pts = generate_random_points(n, x_max, y_max)
            gs_hull, _ = graham_scan(pts[:], _record_steps=False)
            jm_hull, _ = jarvis_march(pts[:], _record_steps=False)
            ca_hull, _ = chans_algo(pts[:], _record_steps=False)
            if set(gs_hull) != set(jm_hull):
                discrepancy = True
                print(f"Trial {i}: Graham's Scan and Jarvis March produced different hulls. GS hull: {gs_hull} with length {len(gs_hull)}, JM hull: {jm_hull} with length {len(jm_hull)}")
            if set(gs_hull) != set(ca_hull):
                discrepancy = True
                print(f"Trial {i}: Graham's Scan and Chan's Algorithm produced different hulls. GS hull: {gs_hull} with length {len(gs_hull)}, CA hull: {ca_hull} with length {len(ca_hull)}")
            if set(jm_hull) != set(ca_hull):
                discrepancy = True
                print(f"Trial {i}: Jarvis March and Chan's Algorithm produced different hulls. JM hull: {jm_hull} with length {len(jm_hull)}, CA hull: {ca_hull} with length {len(ca_hull)}")
            if discrepancy:
                # save the point set and the hulls to a .txt file for debugging
                _save_point_set(pts, trial_num=i)
                break
        if not discrepancy:
            print(f"All {n_trials} trials passed: Graham's Scan and Jarvis March produced the same hulls.")

    if not running_trials:
        # algo_name = "graham_scan"
        # algo_name = "jarvis_march"
        algo_name = "chan_algorithm"
        hull, steps = algos[algo_name]
        visualize(pts, steps, algo_name)

    # plot the final hull as a sanity check
    # hull_xs, hull_ys = zip(*gs_hull)
    # plt.figure(figsize=(10, 8))
    # plt.scatter(xs, ys, color='blue', label='Random Points')
    # plt.plot(hull_xs + (hull_xs[0],), hull_ys + (hull_ys[0],), color='red', label='Convex Hull')
    # plt.title(f"Graham's Scan Final Hull (size: {len(gs_hull)})")
    # plt.xlabel('X-axis')
    # plt.ylabel('Y-axis')
    # plt.legend()
    # plt.grid()
    # plt.show()


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

    # # print the points in pts
    # print("Input points:")
    # for p in pts:
    #     print(p)

    # # plot the hulls produced by each of the three algorithms, side by side for easy comparison
    # fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    # for ax, (algo_name, algo_output) in zip(axs, algos.items()):
    #     print(f"Visualizing {algo_name} output...")
    #     hull, _ = algo_output
    #     xs, ys = zip(*pts)
    #     # print(f"{algo_name} produced a hull with {len(hull)} points.")
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