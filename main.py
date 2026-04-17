# import random
import numpy as np
import matplotlib.pyplot as plt

from geometry import general_position

from benchmark import random_small_hull

from graham import graham_scan
from jarvis import jarvis_march
from chan import chans_algo

def main():
    n = 1000
    x_max = 10000
    y_max = 10000
    # pts = generate_random_points(n, x_max, y_max)
    pts = random_small_hull(n, x_max, y_max)
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

    # hull = graham_scan(pts)
    # hull = jarvis_march(pts)
    hull = chans_algo(pts)
    # print(f"Convex Hull has {len(hull)} points: {hull}")

    hull_xs, hull_ys = zip(*hull)
    plt.figure(figsize=(10, 8))
    plt.scatter(xs, ys, color='blue', label='Random Points')
    plt.plot(hull_xs + (hull_xs[0],), hull_ys + (hull_ys[0],), color='red', label='Convex Hull')
    plt.title('Convex Hull using Graham Scan')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()