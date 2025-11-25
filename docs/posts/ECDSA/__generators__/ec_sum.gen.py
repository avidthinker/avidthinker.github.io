import numpy as np
import matplotlib.pyplot as plt
from misc import (
    plot_segment,
    plot_ec_curve,
    curve_pos_y,
    point_from_x,
    annotate_point,
)

# chooses two points P and Q on the curve (upper branch)
P = point_from_x(-1.5)
Q = point_from_x(2)

# finds intersection point -R
Delta = Q - P
m = Delta[1] / Delta[0]
x = m**2 - P[0] - Q[0]
neg_R = np.array([x, curve_pos_y(x)])

# reflects across X-axis to get R = P + Q
R = neg_R * np.array([1, -1])

plot_ec_curve(-2, 3, color="b", label=r"$y^2 = x^3+7$")
plot_segment([P, Q], style="g--", label="Line through P and Q", t_lims=(-0.2, 1.3))

plt.plot(P[0], P[1], "ko")
plt.plot(Q[0], Q[1], "ko")
plt.plot(neg_R[0], neg_R[1], "rx")
plt.plot(R[0], R[1], "ro")

annotate_point(P, "P", offset=(-4, 7))
annotate_point(Q, "Q", offset=(-4, 7))
annotate_point(neg_R, "-R", color="r", offset=(-7, 7))
annotate_point(R, "R = P + Q", color="r", offset=(-4, 7))

# axes and other labels
plt.axhline(0, color="black", linewidth=0.5)
plt.axvline(0, color="black", linewidth=0.5)
plt.title(r"Elliptic Curve $y^2 = x^3 + 7$ with P, Q, and $R = P+Q$")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.savefig("ec_sum.svg", format="svg", bbox_inches="tight")
