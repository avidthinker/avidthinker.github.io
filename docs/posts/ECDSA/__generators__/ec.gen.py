import matplotlib.pyplot as plt
from misc import plot_ec_curve

plot_ec_curve(-2, 3, 1000, color="blue")

plt.axhline(0, color="black", linewidth=0.5)
plt.axvline(0, color="black", linewidth=0.5)
plt.title(r"Elliptic Curve $y^2 = x^3 + 7$")
plt.xlabel("x")
plt.ylabel("y")
plt.savefig("ec.svg", format="svg", bbox_inches="tight")
