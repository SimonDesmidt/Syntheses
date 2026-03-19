import numpy as np 
import matplotlib.pyplot as plt 

x = np.linspace(-8,8,1000)
integers = np.arange(-8,8)
f = lambda x : x**3/100 - x**2/50+4-x/20-np.sin(x)

plt.figure()
plt.plot(x, f(x), label=r"$x(t)$", color="black")
plt.scatter(integers, f(integers), label=r"$x_T(t)$", color="red", marker="o")
plt.axhline(0, -8,8, color="k", lw=2)
plt.axvline(0, color="k", lw=2)
for i in integers:
    plt.vlines(i, ymin=min(f(i), 0), ymax=max(f(i),0), linestyle="--", color="red")
plt.legend()
# plt.grid()
plt.xlabel("t")
plt.ylabel("x(t)")
plt.savefig("img/sha.pdf", dpi=150)
plt.show()