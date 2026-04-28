import matplotlib.pyplot as plt
from geometry import Point
from typing import List, Dict, Any, Tuple

COLORS = {
    "background": "#ffffff",
    "point": "#1f77b4",
    "current_point": "#ff7f0e",
    "hull_point": "#2ca02c",
    "hull_edge": "#2ca02c",
    "removed_point": "#d62728",
    "text": "#000000",
    "grid": "#cccccc"
}

input_points: List[Point] = []

def setup_ax(ax, points: List[Point], title: str = ""):
    xs, ys = zip(*points)
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    x_range = max(xmax - xmin, 1)
    y_range = max(ymax - ymin, 1)
    padding = 0.1
    ax.set_xlim(xmin - padding * x_range, xmax + padding * x_range)
    ax.set_ylim(ymin - padding * y_range, ymax + padding * y_range)
    
    ax.set_facecolor(COLORS["background"])
    ax.tick_params(colors=COLORS["text"], labelsize=7)


def draw_points(ax, pts: List[Point], color=None, s=35, zorder=3, alpha=1.0, marker="o"):
    padding = 0.1
    xs, ys = zip(*pts)

    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    xr = max(xmax - xmin, 1)
    yr = max(ymax - ymin, 1)
    ax.set_xlim(xmin - padding * xr, xmax + padding * xr)
    ax.set_ylim(ymin - padding * yr, ymax + padding * yr)
    ax.set_facecolor(COLORS["background"])
    ax.tick_params(colors=COLORS["text"], labelsize=7)
    for spine in ax.spines.values():
        spine.set_color(COLORS["grid"])
    ax.grid(color=COLORS["grid"], lw=0.5, alpha=0.5)
    ax.scatter(xs, ys, color=color, s=s, zorder=zorder, alpha=alpha, marker=marker)
    
def draw_hull(ax, hull: List[Point], color=None, lw=2, zorder=4):
    if len(hull) == 0:
        return
    hull_xs, hull_ys = zip(*hull)
    ax.plot(hull_xs + (hull_xs[0],), hull_ys + (hull_ys[0],), color=color, lw=lw, zorder=zorder)

def draw_line(ax, p1: Point, p2: Point, color=None, lw=1, zorder=4):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw, zorder=zorder)

# draws lines connecting the given points in order, without closing the curve
# uses draw_line
def draw_polygonal_curve(ax, points: List[Point], color=None, lw=1, zorder=4):
    for i in range(len(points) - 1):
        draw_line(ax, points[i], points[i+1], color=color, lw=lw, zorder=zorder)
    

# Graham scan
def render_graham_step(ax, step: Dict[str, Any]):
    print("HERE")
    phase = step["phase"]
    stack = step["stack"]
    # current = step["current"]

    setup_ax(ax, input_points)

    if phase == "push":
        draw_points(ax, stack[:-1], color=COLORS["hull_point"], s=50, zorder=4)
        draw_points(ax, [stack[-1]], color=COLORS["current_point"], s=100, zorder=5)
    elif phase == "pop":
        draw_points(ax, stack, color=COLORS["hull_point"], s=50, zorder=4)
        current = step["current"]
        draw_points(ax, [current], color=COLORS["removed_point"], s=100, zorder=5)
    elif phase == "finished_chain":
        draw_points(ax, stack, color=COLORS["hull_point"], s=50, zorder=4)
    elif phase == "finished":
        # draw_points(ax, hull, color=COLORS["hull_point"], s=50, zorder=4)
        draw_hull(ax, stack, color=COLORS["hull_edge"], lw=2, zorder=5)
        return
    else:
        raise ValueError(f"Unknown phase {phase} in step: {step}")
        
    draw_polygonal_curve(ax, stack, color=COLORS["hull_edge"], lw=2, zorder=5)

# Dispatch
RENDERERS = {
    "graham_scan": render_graham_step,
    "jarvis_march": None, # TODO
    "chan_algorithm": None # TODO
}

# Visualizer
class Visualizer:
    def __init__(self, points: List[Point], steps: List[Dict[str, Any]], algorithm: str):
        self.points = points # all input points
        self.steps = steps
        self.algorithm = algorithm
        self.idx = 0 # index of the current step being visualized

        # figure layout: main area + description bar
        # TODO: add nav buttons to step through the visualization
        self.fig = plt.figure(figsize=(10, 8), facecolor=COLORS["background"])

        # main area
        self.ax = self.fig.add_axes([0.05, 0.05, 0.9, 0.9])
        # description bar
        self.desc_ax = self.fig.add_axes([0.05, 0.95, 0.9, 0.05])
        self.desc_ax.axis("off")
        self.desc_text = self.desc_ax.text(0.5, 0.5, "", ha="center", va="center", fontsize=10, color=COLORS["text"])
        # step counter
        self.counter_text = self.desc_ax.text(0.5, 0.05, "", ha="center", color=COLORS["text"], fontsize=8)

    def _render(self):
        step = self.steps[self.idx]
        render_fn = RENDERERS[self.algorithm]
        # render_fn(self.ax, step, self.points)
        render_fn(self.ax, step)
        setup_ax(self.ax, self.points)
        self.desc_text.set_text(step["description"])
        self.counter_text.set_text(f"Step {self.idx + 1} of {len(self.steps)}")
        self.fig.canvas.draw_idle()

def show_steps_auto(steps: List[Dict[str, Any]], points: List[Point], algorithm: str, delay: float = 0.5, title: str = ""):
    fig, ax = plt.subplots(figsize=(8, 6), facecolor=COLORS["background"])
    fig.suptitle(title, color=COLORS["text"], fontsize=11)
    plt.ion()
    render_fn = RENDERERS[algorithm]
    assert render_fn is not None, f"No renderer defined for algorithm {algorithm}"
    assert len(points) > 0, "No input points to visualize"

    global input_points
    input_points.clear()
    input_points.extend(points)

    # draw initial points
    draw_points(ax, points, color=COLORS["point"], s=35, zorder=3)
    plt.pause(delay)

    # print points for debugging
    print(f"Input points: {points}")

    for i, step in enumerate(steps):
        print(f"Rendering step {i+1}/{len(steps)}")
        ax.cla()
        # render_fn(ax, step, points)
        draw_points(ax, points, color=COLORS["point"], s=35, zorder=3)
        render_fn(ax, step)
        setup_ax(ax, points, title=f"Phase: {step['phase']}  ({i+1}/{len(steps)})")
        desc = step.get("description", "")
        ax.set_xlabel(desc, color=COLORS["text"], fontsize=8)
        plt.pause(delay)

    plt.ioff()
    plt.show()

# visualize function
def visualize(points: List[Point], steps: List[Dict[str, Any]], algorithm: str, title: str = ""):
    # TODO: add option for manual step-through with buttons
    show_steps_auto(steps, points, algorithm, title=title, delay=0.1)