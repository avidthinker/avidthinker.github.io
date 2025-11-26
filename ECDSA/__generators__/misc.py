from typing import Callable, Literal
import numpy as np
import matplotlib.pyplot as plt


def curve_pos_y(x):
    return np.sqrt(x**3 + 7)


def curve_y2(x):
    return x**3 + 7


def point_from_x(x, pos=True) -> np.ndarray:
    y = curve_pos_y(x)
    return np.array([x, y if pos else -y])


def plot_ec_curve(
    xmin: float,
    xmax: float,
    num_points: int = 1000,
    *,
    ymax: float | None = None,
    branches: Literal["both", "pos", "neg"] = "both",
    style="",
    **plt_opts
):
    # NOTE: leftmost point = (leftmost_x, 0)
    leftmost_x = -(7 ** (1 / 3))

    # NOTE: starting to draw from the leftmost point makes the curve smoother
    #  in that point.
    xmin = max(xmin, leftmost_x)

    xs = np.linspace(xmin, xmax, num_points)
    y2s = curve_y2(xs)

    mask = y2s >= 0
    if ymax is not None:
        mask &= y2s < ymax * ymax
    xs = xs[mask]
    y2s = y2s[mask]
    ys = np.sqrt(y2s)

    if branches == "pos":
        plt.plot(xs, ys, style, **plt_opts)
    elif branches == "neg":
        plt.plot(xs, -ys, style, **plt_opts)
    elif xmin <= leftmost_x:
        # NOTE: this perfectly joins the positive and negative branches
        xs = np.hstack([xs[::-1], xs])
        ys = np.hstack([ys[::-1], -ys])
        plt.plot(xs, ys, style, **plt_opts)
    else:
        # the joint part is outside the drawing interval
        plt.plot(xs, ys, style, **plt_opts)
        plt.plot(xs, -ys, style, **plt_opts)


def mod_curve(
    p: int,
    x_func: Callable[[int], int],
    y_func: Callable[[int], int],
    *,
    ymin=0,
    ymax: int | None = None
) -> tuple[list[int], list[int]]:
    xs = []
    ys = []

    if ymax is None:
        ymax = p

    for x in range(p):
        rhs = x_func(x) % p
        for y in range(ymin, ymax):
            if y_func(y) % p == rhs:
                xs.append(x)
                ys.append(y)

    return xs, ys


def _plot_segment_2(
    p: np.ndarray,
    q: np.ndarray,
    *,
    style="",
    label,
    t_lims: tuple[float, float] | None = None,
    x_lims: tuple[float, float] | None = None,
    **plt_opts
):
    if x_lims is not None:
        dx = q[0] - p[0]
        if abs(dx) < 1e-14:
            return
        t_lims = tuple((x - p[0]) / dx for x in x_lims)
    elif t_lims is None:
        t_lims = (0, 1)
    p = p[:, np.newaxis]
    q = q[:, np.newaxis]
    t = np.linspace(*t_lims, num=2)[np.newaxis, :]
    points = p + t * (q - p)
    plt.plot(points[0], points[1], style, label=label, **plt_opts)


def plot_segment(
    points: list[np.ndarray],
    *,
    style="",
    label="",
    t_lims: tuple[float, float] | None = None,
    x_lims: tuple[float, float] | None = None,
    **plt_opts
):
    """Plots a segment through collinear points."""
    left_point = min(points, key=lambda p: p[0])
    right_point = max(points, key=lambda p: p[0])
    _plot_segment_2(
        left_point,
        right_point,
        style=style,
        label=label,
        t_lims=t_lims,
        x_lims=x_lims,
        **plt_opts
    )


def annotate_point(P, label: str, *, color: str = "black", offset: tuple[float, float]):
    plt.annotate(
        label,
        (P[0], P[1]),
        textcoords="offset points",
        xytext=offset,
        fontsize=12,
        color=color,
    )
