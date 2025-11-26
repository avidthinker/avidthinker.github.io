import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from misc import (
    point_from_x,
    plot_segment,
    annotate_point,
    plot_ec_curve,
)

num_Qs = 50

# chooses two points P and Q on the curve (upper branch)
P_x = -1.4
dx = 0.4
P = point_from_x(P_x)

point_lims = (P_x - dx, P_x + dx)
xs = np.linspace(0, 1, num=num_Qs)
xs = (2 * (xs - 0.5)) ** 3 / 2
cmap_idxs = (-abs(xs) * 2 + 1) * num_Qs
xs = xs * 2 * dx + P_x

Qs = [point_from_x(x) for x in xs]

cmap = LinearSegmentedColormap.from_list("white_blue", ["white", "blue"], num_Qs)
colors = [cmap(int(cmap_idxs[i])) for i in range(num_Qs)]

extra_t = 0.03
seg_lims = (point_lims[0] - extra_t, point_lims[1] + extra_t)
for Q, color in zip(Qs, colors):
    plot_segment([P, Q], x_lims=seg_lims, linewidth=0.8, color=color)

plot_ec_curve(
    *seg_lims, label=r"$y^2 = x^3+7$", branches="pos", color="black", linewidth=1.5
)

plt.plot(P[0], P[1], "ko", markersize=3)
for Q, color in zip(Qs, colors):
    plt.plot(Q[0], Q[1], color=color, marker="o", markersize=1)

# plots the tangent
tangent_m = 3 * P[0] ** 2 / (2 * P[1])
tangent_ys = tuple((x - P_x) * tangent_m + P[1] for x in seg_lims)
plt.plot(seg_lims, tangent_ys, color="purple", linewidth=1, label="tangent line")

annotate_point(P, "P", offset=(-3, -16))

# axes and other labels
plt.title(r"Elliptic Curve $y^2 = x^3 + 7$ and secants")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.savefig("tangent.svg", format="svg", bbox_inches="tight")
