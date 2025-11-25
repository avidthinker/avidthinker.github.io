import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")


def draw_segment(
    p, q, num_points, style, *, t_lims: tuple[float, float] | None = None, **plt_opts
):
    p = p[:, np.newaxis, np.newaxis]
    q = q[:, np.newaxis, np.newaxis]
    if t_lims is None:
        t_lims = (0, 1)
    t = np.linspace(*t_lims, num=num_points)[np.newaxis, np.newaxis, :]
    points = p + t * (q - p)
    ax.plot(points[0], points[1], points[2], style, **plt_opts)


def curve_pos_y(x, z: float):
    return np.sqrt((x**3 + 7 * z**3) / z)


def curve_y2(x, z: float):
    return (x**3 + 7 * z**3) / z


def get_ec(
    xmin: float, xmax: float, lam: float, *, num_points: int = 1000
) -> tuple[np.ndarray, np.ndarray]:
    # NOTE: leftmost point = (leftmost_x, 0), scaled/reflected by `lam`
    leftmost_x = -(7 ** (1 / 3)) * lam

    if lam < 0:
        xmin, xmax = xmax, xmin
    else:
        xmin = max(xmin, leftmost_x)

    # NOTE: starting to draw from the leftmost point makes the curve smoother
    #  in that point.
    xmin = min(xmin, leftmost_x)

    x_vals = np.linspace(xmin, xmax, num_points)
    x_vals = x_vals[curve_y2(x_vals, lam) >= 0]
    y_vals = curve_pos_y(x_vals, lam)

    # NOTE: this perfectly joins the positive and negative branches
    x_vals = np.hstack([x_vals[::-1], x_vals])
    y_vals = np.hstack([y_vals[::-1], -y_vals])

    return x_vals, y_vals


def plot_ec(
    xmin: float, xmax: float, lam: float, *, num_points: int = 1000, **plt_opts
) -> None:
    x_vals, y_vals = get_ec(xmin, xmax, lam, num_points=num_points)
    ax.plot(x_vals, y_vals, lam, **plt_opts)


def plot_plane(xmin, xmax, ymin, ymax, z, **plt_opts):
    x = np.linspace(xmin, xmax, 10)
    y = np.linspace(ymin, ymax, 10)
    X, Y = np.meshgrid(x, y)
    Z = z * np.ones_like(X)  # constant z-plane
    ax.plot_surface(X, Y, Z, **plt_opts)


lam2 = 2
plot_ec(-2, 3 * lam2, lam=1, color="b")
plot_ec(-2 * lam2, 3 * lam2, lam=lam2, color="g")
plot_ec(-3 * lam2, 2, lam=-1, color="y")
plot_ec(-3 * lam2, 2 * lam2, lam=-lam2, color="r")


def adjust(_min: float, _max: float, scaling: float = 1.0) -> tuple[float, float]:
    _min = min(_min, 0)
    _max = max(_max, 0)
    m = (_min + _max) / 2
    return (_min - m) * scaling + m, (_max - m) * scaling + m


# gets data limits
xmin, xmax = adjust(*ax.get_xlim())
ymin, ymax = adjust(*ax.get_ylim())
zmin, zmax = adjust(*ax.get_zlim())

plot_plane(xmin, xmax, ymin, ymax, lam2, color="g", alpha=0.2, label=f"z = {lam2}")
plot_plane(xmin, xmax, ymin, ymax, 1, color="b", alpha=0.2, label="z = 1")
plot_plane(xmin, xmax, ymin, ymax, 0, color="k", alpha=0.2, label="z = 0")
plot_plane(xmin, xmax, ymin, ymax, -1, color="y", alpha=0.2, label="z = -1")
plot_plane(xmin, xmax, ymin, ymax, -lam2, color="r", alpha=0.2, label=f"z = -{lam2}")

xs, ys = get_ec(-2 * lam2, 3 * lam2, lam=lam2)
for i in range(0, len(xs), len(xs) // 5):
    P = np.array([xs[i], ys[i], lam2])
    Po2 = P / 2
    ax.scatter3D(P[0], P[1], P[2], color="g")
    ax.scatter3D(Po2[0], Po2[1], Po2[2], color="b")
    ax.scatter3D(-Po2[0], -Po2[1], -Po2[2], color="y")
    ax.scatter3D(-P[0], -P[1], -P[2], color="r")
    draw_segment(-P, P, 2, "k--", lw=0.5, t_lims=(0, 1))

# draws custom axes through the origin
scaling = 1.3  # a little longer than the data extent
xmin, xmax = adjust(*ax.get_xlim(), scaling=scaling)
ymin, ymax = adjust(*ax.get_ylim(), scaling=scaling)
zmin, zmax = adjust(*ax.get_zlim(), scaling=scaling)
ax.plot([xmin, xmax], [0, 0], [0, 0], color="k", lw=0.5)  # X-axis
ax.plot([0, 0], [ymin, ymax], [0, 0], color="k", lw=0.5)  # Y-axis
ax.plot([0, 0], [0, 0], [zmin, zmax], color="k", lw=0.5)  # Z-axis
ax.text(xmax, 0, 0, "x", fontsize=12)
ax.text(0, ymax, 0, "y", fontsize=12)
ax.text(0, 0, zmax, "z", fontsize=12)

# shrinks the margins
scaling = 0.6
ax.set_xlim(*adjust(*ax.get_xlim(), scaling=scaling))
ax.set_ylim(*adjust(*ax.get_ylim(), scaling=scaling))
ax.set_zlim(*adjust(*ax.get_zlim(), scaling=scaling))

ax.set_axis_off()
ax.view_init(elev=15, azim=-60, roll=0)
fig.tight_layout(pad=0)
fig.legend()
ax.set_box_aspect([1, 1, 1])  # equal aspect ratio, no extra padding
plt.savefig("ec_proj.svg", format="svg", bbox_inches="tight")
