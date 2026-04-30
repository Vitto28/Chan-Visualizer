import time
import numpy as np
import math

from geometry import Point, List, general_position

from graham import graham_scan
from jarvis import jarvis_march
from chan import chans_algo

# TODO: define strategies separately

algos = {
    "Graham's Scan": graham_scan,
    "Jarvis March": jarvis_march,
    "Chan's Algorithm": chans_algo
}

# === Point generation strategies ===

def rnd_pts(n=20, max=100, seed=None):
    return np.random.permutation(max)[:n]

def generate_random_points(n=20, x_max=400, y_max=300, seed=None):
    while True:
        x_rng = rnd_pts(n, x_max, seed)
        y_rng = rnd_pts(n, y_max, seed)
        pts = list(zip(x_rng, y_rng))
        # pts = [(rng.randint(0, x_max), rng.randint(0, y_max)) for _ in range(n)]
        if general_position(pts):
            break
    return pts

# === Complex configurations of points ===

def random_circle(n: int, x_max=1000, y_max=1000, radius=300, seed=None) -> List[Point]:
    """ Points in a circle configuration, which is a worst-case scenario for Jarvis March since all points are on the hull. """
    rng = np.random.default_rng(seed)
    center = (x_max // 2, y_max // 2)
    points = []
    for _ in range(n):
        angle = rng.uniform(0, 2 * math.pi)
        x = int(center[0] + radius * math.cos(angle))
        y = int(center[1] + radius * math.sin(angle))
        points.append((x, y))
    return points

def random_small_hull(n: int, x_max=1000, y_max=1000, seed=None) -> List[Point]:
    """ Random points with a small hull, which is a best-case scenario for Jarvis March since it will only have to find a few hull points. The rest of the points will be clustered around the center, so they won't be on the hull. """
    # hull size should be < log n for Jarvis to be better than Graham
    # hull_size = max(3, int(math.log2(n) // 2)) # ensure hull size is at least 3
    hull_size = max(3, int(np.floor(math.log2(n)))-1) # ensure hull size is at least 3
    # print(f"Generating {hull_size} hull points and {n - hull_size} interior points.")

    rng = np.random.default_rng(seed)
    center = (x_max // 2, y_max // 2)
    points = []
    # generate hull points in a circle around the center
    for i in range(hull_size):
        angle = 2 * math.pi * i / hull_size
        x = int(center[0] + 300 * math.cos(angle))
        y = int(center[1] + 300 * math.sin(angle))
        points.append((x, y))
    # generate the rest of the points clustered around the center
    for _ in range(n - hull_size):
        x = int(center[0] + rng.normal(0, 50)) # cluster around the center with some noise
        y = int(center[1] + rng.normal(0, 50))
        points.append((x, y))
    return points



# === Benchmarking framework ===

# TODO: this doesnt check that the hulls produced by the algorithms are correct, nor that they are equal to each other, which they should be. maybe add a check to verify that the hulls are correct and consistent with each other, to catch any potential bugs in the implementations?
def run_benchmark_config(config_func, sizes, trials):
    print(f"\nBenchmarking configuration: {config_name}")
    for algo_name, algo_func in algos.items():
        print(f"Benchmarking {algo_name} on {config_name}...")
        for n in sizes:
            times = []
            for _ in range(trials):
                pts = config_func(n=n)
                start_time = time.time()
                algo_func(pts)
                end_time = time.time()
                times.append(end_time - start_time)
            avg_time = sum(times) / trials
            config_times[config_name][algo_name].append(avg_time)
            # print(f"Average time for n={n}: {avg_time:.6f} seconds")

    # TODO: should be a toggable option?
    print(f"\nResults for configuration: {config_name}")
    print(f"{'Input size':>10}", end="")
    # print(f"{'Hull size':>20}", end="")
    for algo_name in algos.keys():
        print(f"{algo_name:>20}", end="")
    print(f"{'Best':>20}", end="")
    print(f"{"Worst":>20}", end="")
    print()
    for i, n in enumerate(sizes):
        print(f"{n:>10}", end="")
        for algo_name in algos.keys():
            print(f"{config_times[config_name][algo_name][i]:>20.6f}", end="")
        best_algo = min(algos.keys(), key=lambda name: config_times[config_name][name][i])
        print(f"{best_algo:>20}", end="")
        worst_algo = max(algos.keys(), key=lambda name: config_times[config_name][name][i])
        print(f"{worst_algo:>20}", end="")
        print()

# === Main benchmarking function ===

def run_benchmark(sizes, trials):
    # avg times per algo per size

    # print experiment setup
    print("Benchmarking Convex Hull Algorithms")
    print(f"Sizes: {sizes}")
    print(f"Trials per size: {trials}")
    print(f"Algorithms: {list(algos.keys())}")

    avg_times = {algo_name: [] for algo_name in algos.keys()}

    for algo_name, algo_func in algos.items():
        # print(f"Benchmarking {algo_name}...")
        for n in sizes:
            # pts = generate_random_points(n=n, x_max=1000, y_max=1000)
            times = []
            print(f"Benchmarking {algo_name} with n={n} points...")
            for _ in range(trials):
                pts = generate_random_points(n=n, x_max=1000, y_max=1000)
                start_time = time.time()
                # print(f"Running {algo_name} on {n} points...")
                algo_func(pts)
                end_time = time.time()
                times.append(end_time - start_time)
            avg_time = sum(times) / trials
            avg_times[algo_name].append(avg_time)

            # print(f"Average time for n={n}: {avg_time:.6f} seconds")

    return avg_times

# === Main execution ===

if __name__ == "__main__":
    # sizes = [10, 20, 50, 100, 200, 500, 1000]
    sizes = [10000]
    # TODO: aside from random points, also try other distributions (e.g. points on a circle, points in a grid, etc.)
    # since jarvis depends on the number of hull points, so it can potentially perform much better/worse on certain distributions (e.g. points on a circle, where all points are on the hull)
    trials = 10 # number of trials to average over for each size
    times = run_benchmark(sizes, trials)

    # TODO: rewrite this portion to use the run_benchmark_config function, to avoid code dup

    # print a summary of the results as a nice table
    print("\nBenchmark Results:")
    print(f"{'Input size':>10}", end="")
    # print(f"{'Hull size':>20}", end="")
    for algo_name in algos.keys():
        print(f"{algo_name:>20}", end="")
    print(f"{'Best':>20}", end="")
    print(f"{"Worst":>20}", end="")
    print()
    for i, n in enumerate(sizes):
        print(f"{n:>10}", end="")
        for algo_name in algos.keys():
            print(f"{times[algo_name][i]:>20.6f}", end="")
        # print the name of the algo with the best time for this size
        best_algo = min(algos.keys(), key=lambda name: times[name][i])
        worst_algo = max(algos.keys(), key=lambda name: times[name][i])
        print(f"{best_algo:>20}", end="")
        print(f"{worst_algo:>20}", end="")
        print()

    # === More complex configurations of points ===
    configs = {
        "Points in a circle": random_circle,
        "Random points with a small hull": random_small_hull
    }

    # do as before, but then each row is like circle(50), circle(100), etc. instead of just 50, 100, etc.
    # save the times for each config in a separate dictionary
    config_times = {config_name: {algo_name: [] for algo_name in algos.keys()} for config_name in configs.keys()}

    # TODO: make the random generation callable like this
    for config_name, config_func in configs.items():
        run_benchmark_config(config_func, sizes, trials)