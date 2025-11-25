import matplotlib.pyplot as plt
from misc import plot_ec_curve, mod_curve

p = 97

xs, ys = mod_curve(p, lambda x: x**3 + 7, lambda y: y * y)
plt.scatter(xs, ys, s=50)

plot_ec_curve(0, p, ymax=p, branches="pos", color="b")

plt.title(rf"Elliptic Curve $y^2 = x^3 + 7\ (\mathrm{{mod}}\ {p})$")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True, which="both")
plt.savefig("ec_mod_p.svg", format="svg", bbox_inches="tight")
