import random
import matplotlib.pyplot as plt

from graham import graham_scan


def main():
    seed = 42
    n = 20
    x_max = 400
    y_max = 300
    # rng = random.Random()
    rng = random.Random(seed)
    pts = [(rng.randint(0, x_max), rng.randint(0, y_max)) for _ in range(n)]
    print(f"Generated {len(pts)} random points.")

    fig = plt.figure(figsize=(10, 8))
    xs, ys = zip(*pts)
    plt.scatter(xs, ys, color='blue', label='Random Points')
    plt.title('Random Points')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid()
    plt.show()

    hull = graham_scan(pts)
    print(f"Convex Hull has {len(hull)} points: {hull}")

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