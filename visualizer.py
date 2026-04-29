import matplotlib.pyplot as plt
from geometry import Point
from typing import List, Dict, Any, Tuple

from matplotlib.widgets import Button

COLORS = {
    "background": "#ffffff",
    "point": "#1f77b4",
    "current_point": "#ff7f0e",
    "hull_point": "#2ca02c",
    "hull_edge": "#2ca02c",
    "potential_hull_edge": "#ff7f0e",
    "potential_hull_vertex": "#ff7f0e",
    "best_candidate_edge": "#1f77b4",
    "removed_point": "#d62728",
    "text": "#000000",
    "grid": "#cccccc"
}

input_points: List[Point] = []

# === Drawing utilities ===

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
    
# === Algorithm-specific renderers ===

# Graham scan
def render_graham_step(ax, step: Dict[str, Any]):
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


def render_jarvis_step(ax, step: Dict[str, Any]):
    phase = step["phase"]
    stack = step["stack"]

    setup_ax(ax, input_points)
    # always draw the current hull points
    draw_polygonal_curve(ax, stack, color=COLORS["hull_edge"], lw=2, zorder=4)

    if phase == "start":
        current = step["current"]
        sentinel = step["sentinel"]
        draw_points(ax, [current], color=COLORS["current_point"], s=100, zorder=5)
        draw_points(ax, [sentinel], color=COLORS["removed_point"], s=100, zorder=5)
    elif phase == "candidate_test":
        pivot = step["pivot"]
        pivot_pred = step["pivot_pred"]
        candidate = step["candidate"]
        current_best = step.get("current_best", None)

        # draw_points(ax, stack, color=COLORS["hull_point"], s=50, zorder=4)
        draw_points(ax, [pivot], color=COLORS["current_point"], s=100, zorder=5)
        draw_points(ax, [candidate], color=COLORS["potential_hull_vertex"], s=100, zorder=5)
        if current_best is not None:
            draw_points(ax, [current_best], color=COLORS["hull_point"], s=100, zorder=6)
        draw_line(ax, pivot_pred, pivot, color=COLORS["hull_edge"], lw=2, zorder=4)
        draw_line(ax, pivot, candidate, color=COLORS["potential_hull_edge"], lw=2, zorder=5)
        if current_best is not None:
            draw_line(ax, pivot, current_best, color=COLORS["hull_edge"], lw=2, zorder=6)
    elif phase == "new_best":
        pivot = step["pivot"]
        pivot_pred = step["pivot_pred"]
        new_best = step["new_best"]

        # draw_points(ax, stack, color=COLORS["hull_point"], s=50, zorder=4)
        draw_points(ax, [pivot], color=COLORS["current_point"], s=100, zorder=5)
        draw_points(ax, [new_best], color=COLORS["hull_point"], s=100, zorder=6)
        draw_line(ax, pivot_pred, pivot, color=COLORS["hull_edge"], lw=2, zorder=4)
        draw_line(ax, pivot, new_best, color=COLORS["hull_edge"], lw=2, zorder=6)
    elif phase == "current_hull":
        # draw_points(ax, stack, color=COLORS["hull_point"], s=50, zorder=4)
        draw_points(ax, [stack[-1]], color=COLORS["current_point"], s=100, zorder=5)
        draw_polygonal_curve(ax, stack, color=COLORS["hull_edge"], lw=2, zorder=5)
    elif phase == "finished":
        # draw_points(ax, stack, color=COLORS["hull_point"], s=50, zorder=4)
        draw_hull(ax, stack, color=COLORS["hull_edge"], lw=2, zorder=5)
    else:
        raise ValueError(f"Unknown phase {phase} in step: {step}")

# Dispatch
RENDERERS = {
    "graham_scan": render_graham_step,
    "jarvis_march": render_jarvis_step,
    "chan_algorithm": None # TODO
}

# Visualizer
class Visualizer:
    def __init__(self, points: List[Point], steps: List[Dict[str, Any]], algorithm: str):
        self.points = points # all input points
        self.steps = steps
        self.algorithm = algorithm
        self.idx = 0 # index of the current step being visualized

        global input_points
        input_points.clear()
        input_points.extend(points)

        # Figure layout: main plot + description bar + nav buttons
        self.fig = plt.figure(figsize=(10, 7.5), facecolor=COLORS["background"])
        self.fig.suptitle("", color=COLORS["text"], fontsize=11, y=0.97)

        self.ax = self.fig.add_axes([0.06, 0.18, 0.88, 0.74])

        # Description text
        self.desc_ax = self.fig.add_axes([0.06, 0.10, 0.88, 0.06])
        self.desc_ax.set_facecolor("#0d0d1a")
        self.desc_ax.axis("off")
        self.desc_text = self.desc_ax.text(
            0.01, 0.5, "", transform=self.desc_ax.transAxes,
            color=COLORS["text"], fontsize=8.5, va="center",
            fontfamily="monospace",
        )

        # Step counter
        self.counter_text = self.fig.text(
            0.5, 0.05, "", ha="center", color=COLORS["text"], fontsize=8,
        )

        # nav buttons (prev, next, start, end, play/pause)
        ax_prev = self.fig.add_axes([0.20, 0.01, 0.10, 0.05])
        ax_next = self.fig.add_axes([0.34, 0.01, 0.10, 0.05])
        ax_start = self.fig.add_axes([0.06, 0.01, 0.10, 0.05])
        ax_end  = self.fig.add_axes([0.48, 0.01, 0.10, 0.05])
        ax_auto  = self.fig.add_axes([0.82, 0.01, 0.10, 0.05])

        # btn_style = dict(color="#16213e", hovercolor="#0f3460")
        btn_style = dict(color=COLORS["background"])
        self.btn_prev  = Button(ax_prev,  "◀  Prev",  **btn_style)
        self.btn_next  = Button(ax_next,  "Next  ▶", **btn_style)
        self.btn_first = Button(ax_start, "⏮ Start",  **btn_style)
        self.btn_last  = Button(ax_end,  "end ⏭",  **btn_style)
        self.btn_auto  = Button(ax_auto,  "Play/Pause", **btn_style)
        
        for btn in (self.btn_prev, self.btn_next, self.btn_first,
            self.btn_last, self.btn_auto):
            btn.label.set_color(COLORS["text"])
            btn.label.set_fontsize(8)

        self.btn_prev.on_clicked(lambda _: self._go(-1))
        self.btn_next.on_clicked(lambda _: self._go(+1))
        self.btn_first.on_clicked(lambda _: self._jump(0))
        self.btn_last.on_clicked(lambda _: self._jump(len(self.steps) - 1))
        self.btn_auto.on_clicked(lambda _: self._toggle_auto())

        self.fig.canvas.mpl_connect("key_press_event", self._on_key)
        self._render()

    # button handlers
    def _go(self, delta):
        self.idx = max(0, min(len(self.steps) - 1, self.idx + delta))
        self._render()

    def _jump(self, idx):
        self.idx = idx
        self._render()

    def _toggle_auto(self):
        #TODO: implement play/pause functionality
        pass

    def _on_key(self, event):
        if event.key in ("right", "n"):
            self._go(+1)
        elif event.key in ("left", "p"):
            self._go(-1)
        elif event.key == "home":
            self._jump(0)
        elif event.key == "end":
            self._jump(len(self.steps) - 1)
        elif event.key == " ":
            self._toggle_auto()

    def _render(self):
        step = self.steps[self.idx]
        self.ax.cla() # clear the axes before redrawing
        render_fn = RENDERERS[self.algorithm]

        # draw all the points first (some renderers may choose to redraw them, but this ensures the points are always in the background)
        draw_points(self.ax, self.points, color=COLORS["point"], s=35, zorder=3)

        render_fn(self.ax, step)
        setup_ax(self.ax, self.points,
                  title=f"Phase: {step['phase']}")
        self.desc_text.set_text(step.get("description", ""))
        self.counter_text.set_text(
            f"Step {self.idx + 1} / {len(self.steps)}"
        )
        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()

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
    # show_steps_auto(steps, points, algorithm, title=title, delay=0.1)
    vis = Visualizer(points, steps, algorithm)
    vis.show()