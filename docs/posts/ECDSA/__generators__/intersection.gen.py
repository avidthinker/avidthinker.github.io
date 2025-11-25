import numpy as np
import matplotlib.pyplot as plt
from misc import (
    point_from_x,
    curve_pos_y,
    plot_segment,
    annotate_point,
    plot_ec_curve,
)

# chooses two points P and Q on the curve (upper branch)
P = point_from_x(-1.5)
P[1] = -P[1]
Q = point_from_x(-1.49)

# finds intersection point -R
Delta = Q - P
m = Delta[1] / Delta[0]
x = m**2 - P[0] - Q[0]
neg_R = np.array([x, curve_pos_y(x)])

# extra drawing on the right of the intersection point
extra_t = 0.3

plot_ec_curve(-2, neg_R[0] * (1 + extra_t), color="b", label=r"$y^2 = x^3+7$")
plot_segment(
    [P, neg_R], style="g--", label="Line through P and Q", t_lims=(0, 1 + extra_t)
)

plt.plot(P[0], P[1], "ko", markersize=0)
plt.plot(Q[0], Q[1], "ko", markersize=0)
plt.plot(neg_R[0], neg_R[1], "rx")

annotate_point(P, "P", offset=(-3, -16))
annotate_point(Q, "Q", offset=(-5.5, 7))
annotate_point(neg_R, "-R", color="r", offset=(-7, 7))

# axes and other labels
plt.axhline(0, color="black", linewidth=0.5)
plt.axvline(0, color="black", linewidth=0.5)
plt.title('Case with P and Q "almost vertically aligned"')
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.savefig("intersection.svg", format="svg", bbox_inches="tight")
