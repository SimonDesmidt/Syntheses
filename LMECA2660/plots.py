import numpy as np
import matplotlib.pyplot as plt 

def stability_of_centered_diff_in_convection_diffusion_eq():
    R = np.linspace(0,4,200)
    r = np.minimum(0.5, 2 / R**2)
    t = 2/R[3*len(R)//8:len(R)//2]**2

    plt.figure()

    plt.plot(R, r, label="r")
    plt.plot(R[3*len(R)//8:len(R)//2], t, linestyle="--", color="blue")
    plt.fill_between(R, r, hatch='///', alpha=0.15)
    plt.text(1.2, 0.3, "stable", ha='center', va='center', fontsize=14)

    plt.grid()
    plt.ylim(0,1)
    plt.xlabel(r"$R$")
    plt.ylabel(r"$r$")
    plt.tight_layout()
    plt.savefig("img/ellipse.pdf")

def AB(rk4=False):
    AB_COEFFS = {
        1: [1],
        2: [3/2, -1/2],
        3: [23/12, -16/12, 5/12],
        4: [55/24, -59/24, 37/24, -9/24],
        5: [1901/720, -2774/720, 2616/720, -1274/720, 251/720],
        6: [4277/1440, -7923/1440, 9982/1440, -7298/1440, 2877/1440, -475/1440],
    }

    theta_clip = {4: 2.0313503185, 5: 2.3194436403, 6: 2.4917224146}
    
    def rk4_stability_function(z):
        return 1 + z + z**2 / 2 + z**3 / 6 + z**4 / 24

    def stability_boundary_ab(order, n=4000):
        beta = np.array(AB_COEFFS[order], dtype=float)

        if order in theta_clip:
            a = theta_clip[order]
            theta = np.linspace(a, 2 * np.pi - a, n)
        else:
            theta = np.linspace(0, 2 * np.pi, n)

        xi = np.exp(1j * theta)

        rho = xi**order - xi**(order - 1)
        sigma = sum(beta[j] * xi**(order - 1 - j) for j in range(order))

        return rho / sigma

    plt.figure(figsize=(8, 7))
    colors = ["blue", "orange", "green", "red", "purple", "brown"]
    for order in range(1, 7):
        z = stability_boundary_ab(order)
        plt.plot(z.real, z.imag, label=f"AB{order}", color=colors[order-1], linewidth=1.5)

    plt.axhline(0, linewidth=0.8)
    plt.axvline(0, linewidth=0.8)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.grid(True)
    plt.xlabel(r"$\operatorname{Re}(\lambda\Delta t)$")
    plt.ylabel(r"$\operatorname{Im}(\lambda\Delta t)$")
    plt.axvline(0, color="k", linewidth=2.0)
    plt.axhline(0, color="k", linewidth=2.0)
    if rk4:
        x = np.linspace(-4, 1, 900)
        y = np.linspace(-3, 3, 900)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        RK4 = np.abs(rk4_stability_function(Z))
        plt.contour(X, Y, RK4, levels=[1], linewidths=1.5, colors="salmon")
        plt.text(0.4, 2.0, "RK4", color="salmon")
        plt.tight_layout()
        plt.savefig("img/AB_RK4_stability.pdf")
    else : 
        plt.text(-1.7, 0.6, "AB1", color=colors[0])
        plt.text(-1.0, 0.5, "AB2", color=colors[1])
        plt.text(-0.5, 0.45, "AB3", color=colors[2])
        plt.text(-.25, 0.35, "AB4", color=colors[3])
        plt.text(-.15, 0.2, "AB5", color=colors[4])
        plt.text(0.02, 0.05, "AB6", color=colors[5])
        
        plt.tight_layout()
        plt.savefig("img/adams_bashforth_stability.pdf")

def AM(rk4=False, small=False):
    AM_COEFFS = {
        3: [5/12, 2/3, -1/12],
        4: [3/8, 19/24, -5/24, 1/24],
        5: [251/720, 646/720, -264/720, 106/720, -19/720],
        6: [475/1440, 1427/1440, -798/1440, 482/1440, -173/1440, 27/1440],
    }

    def rk4_stability_function(z):
        return 1 + z + z**2 / 2 + z**3 / 6 + z**4 / 24

    def stability_boundary_am(order, n=4000):
        beta = np.array(AM_COEFFS[order], dtype=float)
        s = order - 1
        theta = np.linspace(0, 2 * np.pi, n)

        xi = np.exp(1j * theta)

        rho = xi**s - xi**(s - 1)
        sigma = sum(beta[j] * xi**(s - j) for j in range(order))

        return rho / sigma

    plt.figure(figsize=(8, 7))

    colors = {3: "green", 4: "red", 5: "purple", 6: "brown"}

    for order in range(3, 7):
        z = stability_boundary_am(order)
        plt.plot(z.real, z.imag, label=f"AM{order}", color=colors[order], linewidth=1.5)

    plt.gca().set_aspect("equal", adjustable="box")
    plt.grid(True)
    plt.xlabel(r"$\operatorname{Re}(\lambda\Delta t)$")
    plt.ylabel(r"$\operatorname{Im}(\lambda\Delta t)$")

    title="img/adams_moulton_stability"
    if rk4:
        x = np.linspace(-7, 2, 900)
        y = np.linspace(-4, 4, 900)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        RK4 = np.abs(rk4_stability_function(Z))

        plt.contour(X, Y, RK4, levels=[1], linewidths=1.5, colors="salmon")
        plt.text(-2.7, 2.7, "RK4", color="salmon")
        title += "_RK4"
    
    if small: 
        plt.xlim(-0.4, 0.1)
        plt.ylim(0.0, 1.5)
        plt.legend()
        title += "_small"
    else : 
        plt.text(-5.6, 1.0, "AM3", color=colors[3])
        plt.text(-2.8, 0.75, "AM4", color=colors[4])
        plt.text(-1.6, 0.85, "AM5", color=colors[5])
        plt.text(-0.9, 1.0, "AM6", color=colors[6])
        plt.axvline(0, color="k", linewidth=2.0)
        plt.axhline(0, color="k", linewidth=2.0)
    
    plt.tight_layout()
    plt.savefig(title + ".pdf")

def custom_scheme_stability():
    alphas = [0.25, 0.5, 0.75, 1.0]
    colors = ["blue", "orange", "green", "red"]

    def stability_boundary(alpha, n=4000):
        theta = np.linspace(0, 2 * np.pi, n)
        xi = np.exp(1j * theta)

        numerator = 2 * (xi**2 - alpha * xi - (1 - alpha))
        denominator = (4 - alpha) * xi - alpha

        return numerator / denominator

    plt.figure(figsize=(8, 7))

    for alpha, color in zip(alphas, colors):
        z = stability_boundary(alpha)
        plt.plot(z.real, z.imag, label=rf"$\alpha={alpha}$", color=color, linewidth=1.5)

    plt.gca().set_aspect("equal", adjustable="box")
    plt.grid(True, linestyle=".")
    plt.xlabel(r"$\operatorname{Re}(\lambda\Delta t)$")
    plt.ylabel(r"$\operatorname{Im}(\lambda\Delta t)$")
    plt.axvline(0, color="k", linewidth=2.0)
    plt.axhline(0, color="k", linewidth=2.0)

    plt.text(-0.2, 0.10, r"$\alpha=1/4$", color=colors[0])
    plt.text(-.45, 0.10, r"$\alpha=1/2$", color=colors[1])
    plt.text(-.70, 0.10, r"$\alpha=3/4$", color=colors[2])
    plt.text(-.95, 0.10, r"$\alpha=1$", color=colors[3])

    plt.tight_layout()
    plt.savefig("img/multistep_family_stability.pdf")
    plt.show()

def richtmeyer():
    plt.figure(figsize=(10, 6))
    # Grid levels
    y_n = 0
    y_half = 1
    y_np1 = 2

    # Nodes
    bottom_x = [-1, 0, 1]
    half_x = [-0.5, 0.5]
    top_x = [0]

    # Draw time levels
    plt.plot([-1.25, 1.25], [y_n, y_n], lw=1.5)
    plt.plot([-0.75, 0.75], [y_half, y_half], lw=1.5)
    plt.plot([-0.35, 0.35], [y_np1, y_np1], lw=1.5)

    # Draw nodes
    plt.scatter(bottom_x, [y_n] * len(bottom_x), s=70, zorder=3)
    plt.scatter(half_x, [y_half] * len(half_x), marker="*", s=180, zorder=4)
    plt.scatter(top_x, [y_np1], s=80, zorder=5)

    # Predictor arrows: values at time n produce half-time interface states
    arrowprops = dict(arrowstyle="->", lw=1.4, shrinkA=6, shrinkB=6)
    for x0, x1 in [(-1, -0.5), (0, -0.5), (0, 0.5), (1, 0.5)]:
        plt.annotate("", xy=(x1, y_half), xytext=(x0, y_n), arrowprops=arrowprops)

    # Corrector arrows: half-time fluxes update the central node
    for x0 in half_x:
        plt.annotate("", xy=(0, y_np1), xytext=(x0, y_half), arrowprops=arrowprops)

    # Labels on grid
    plt.text(-1, y_n - 0.18, r"$i-1$", ha="center", va="top", fontsize=14)
    plt.text(0, y_n - 0.18, r"$i$", ha="center", va="top", fontsize=14)
    plt.text(1, y_n - 0.18, r"$i+1$", ha="center", va="top", fontsize=14)

    plt.text(-0.5, y_half + 0.16, r"$i-\frac{1}{2}$", ha="center", va="bottom", fontsize=14)
    plt.text(0.5, y_half + 0.16, r"$i+\frac{1}{2}$", ha="center", va="bottom", fontsize=14)

    plt.text(1.32, y_n, r"$n$", ha="left", va="center", fontsize=14)
    plt.text(0.82, y_half, r"$n+\frac{1}{2}$", ha="left", va="center", fontsize=14)
    plt.text(0.42, y_np1, r"$n+1$", ha="left", va="center", fontsize=14)

    # axis arrows
    plt.annotate("", xy=(-1.45, 2.35), xytext=(-1.45, -0.45), arrowprops=dict(arrowstyle="->", lw=1.8))
    plt.annotate("", xy=(-1.0, -0.45), xytext=(-1.45, -0.45), arrowprops=dict(arrowstyle="->", lw=1.8))
    plt.text(-1.52, 2.42, r"$t$", fontsize=16)
    plt.text(-0.94, -0.52, r"$x$", fontsize=16)

    plt.xlim(-1.65, 1.9)
    plt.ylim(-1.35, 2.9)
    plt.axis("off")

    plt.tight_layout()
    plt.savefig("img/richtmeyer.pdf", dpi=200, bbox_inches="tight")

def mccormack():
    from matplotlib.patches import FancyArrowPatch

    fig, ax = plt.subplots(figsize=(11, 4.8))

    # Grid coordinates
    x_im1, x_i, x_ip1 = -1, 0, 1
    y_n, y_np1 = 0, 1

    # Draw grid lines
    ax.plot([-1.35, 1.35], [y_n, y_n], lw=1.5)
    ax.plot([-1.35, 1.35], [y_np1, y_np1], lw=1.5)

    # Draw grid nodes
    ax.scatter([x_im1, x_i, x_ip1], [y_n, y_n, y_n], s=70, zorder=4)
    ax.scatter([x_im1, x_i, x_ip1], [y_np1, y_np1, y_np1], s=70, zorder=4)

    # Helper for arrows
    def arrow(x0, y0, x1, y1, lw=2.2, mutation_scale=18, connectionstyle="arc3"):
        ax.add_patch(FancyArrowPatch((x0, y0),(x1, y1),arrowstyle="->",lw=lw,mutation_scale=mutation_scale,shrinkA=6,shrinkB=6,connectionstyle=connectionstyle))

    # Predictor: forward-difference paths from time n to predicted values at n+1
    arrow(x_im1, y_n, x_im1, y_np1)
    arrow(x_i, y_n, x_im1, y_np1)
    arrow(x_i, y_n, x_i, y_np1)
    arrow(x_ip1, y_n, x_i, y_np1)

    # Highlighted right predictor for s_i*
    arrow(x_ip1, y_n, x_i, y_np1, lw=2.5)
    ax.text(0.48, 0.58, "predictor", rotation=180+138+6, fontsize=13, ha="center", va="center")

    # Corrector: average original and predicted values back to final value at i
    arc = FancyArrowPatch((x_im1, y_np1 + 0.02),(x_i, y_np1 + 0.02),arrowstyle="->",lw=2.4,mutation_scale=18,shrinkA=8,shrinkB=8,connectionstyle="arc3,rad=-0.25")
    ax.add_patch(arc)
    ax.text(-0.48, 1.24, "corrector", fontsize=13, ha="center", va="bottom")

    # Labels
    ax.text(x_im1, y_n - 0.12, r"$i-1$", ha="center", va="top", fontsize=15)
    ax.text(x_i, y_n - 0.12, r"$i$", ha="center", va="top", fontsize=15)
    ax.text(x_ip1, y_n - 0.12, r"$i+1$", ha="center", va="top", fontsize=15)

    ax.text(1.68, y_n, r"$n$", ha="left", va="center", fontsize=15)
    ax.text(1.68, y_np1, r"$n+1$", ha="left", va="center", fontsize=15)

    ax.text(x_im1 - 0.12, y_np1 + 0.12, r"$\tilde{s}_{i-1}^{\,n+1}$", ha="center", fontsize=15)
    ax.text(x_i + 0.05, y_np1 + 0.12, r"$\tilde{s}_{i}^{*}; \tilde{s}_i^{n+1}$", ha="center", fontsize=15)

    # Axis arrows
    ax.annotate("", xy=(-1.58, 1.28), xytext=(-1.58, -0.25), arrowprops=dict(arrowstyle="->", lw=1.8))
    ax.annotate("", xy=(-1.18, -0.25), xytext=(-1.58, -0.25), arrowprops=dict(arrowstyle="->", lw=1.8))
    ax.text(-1.65, 1.32, r"$t$", fontsize=16)
    ax.text(-1.12, -0.30, r"$x$", fontsize=16)

    ax.set_xlim(-1.85, 2.2)
    ax.set_ylim(-0.85, 1.72)
    ax.axis("off")

    plt.tight_layout()
    plt.savefig("img/mccormack.pdf", dpi=200, bbox_inches="tight")

def mac():
    nx, ny = 3, 3

    fig, ax = plt.subplots(figsize=(6.5, 5.4))

    # Cell grid
    for i in range(nx + 1):
        ax.plot([i, i], [0, ny], lw=1.4)
    for j in range(ny + 1):
        ax.plot([0, nx], [j, j], lw=1.4)

    # Pressure / scalar locations at cell centers
    xc = np.arange(nx) + 0.5
    yc = np.arange(ny) + 0.5
    Xc, Yc = np.meshgrid(xc, yc)
    ax.scatter(Xc, Yc, s=85, marker="o", zorder=4, label=r"$p_{i,j}$")

    # u velocity on vertical faces
    xu = np.arange(nx + 1)
    yu = np.arange(ny) + 0.5
    Xu, Yu = np.meshgrid(xu, yu)
    ax.scatter(Xu, Yu, s=115, marker=">", zorder=5, label=r"$u_{i+1/2,j}$")

    # v velocity on horizontal faces
    xv = np.arange(nx) + 0.5
    yv = np.arange(ny + 1)
    Xv, Yv = np.meshgrid(xv, yv)
    ax.scatter(Xv, Yv, s=115, marker="^", zorder=5, label=r"$v_{i,j+1/2}$")

    # Highlight central cell
    i, j = 1, 1
    ax.add_patch(plt.Rectangle((i, j), 1, 1, fill=False, lw=3, zorder=3))
    ax.text(i + 0.5, j + 0.5, r"$p_{i,j}$", ha="center", va="center", fontsize=15, zorder=10)
    ax.text(i, j + 0.5, r"$u_{i-\frac{1}{2},j}$", ha="right", va="center", fontsize=12, zorder=10)
    ax.text(i + 1, j + 0.5, r"$u_{i+\frac{1}{2},j}$", ha="left", va="center", fontsize=12, zorder=10)
    ax.text(i + 0.5, j, r"$v_{i,j-\frac{1}{2}}$", ha="center", va="top", fontsize=12, zorder=10)
    ax.text(i + 0.5, j + 1, r"$v_{i,j+\frac{1}{2}}$", ha="center", va="bottom", fontsize=12, zorder=10)

    ax.set_aspect("equal")
    ax.set_xlim(-0.35, nx + 0.65)
    ax.set_ylim(-0.55, ny + 0.35)
    ax.axis("off")
    ax.legend(loc="upper right", frameon=True, fontsize=11)

    fig.savefig("img/mac_mesh.pdf", dpi=220, bbox_inches="tight")
    plt.show()

    
if __name__ == "__main__":
    # stability_of_centered_diff_in_convection_diffusion_eq()
    # AB(False)
    # AB(True)
    # AM(False)
    # AM(True)
    # AM(False, True)
    # custom_scheme_stability()
    # richtmeyer()
    # mccormack()
    mac()
    plt.show()