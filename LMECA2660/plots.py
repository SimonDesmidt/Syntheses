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
    plt.savefig("img/ellipse.png")

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
        plt.savefig("img/AB_RK4_stability.png")
    else : 
        plt.text(-1.7, 0.6, "AB1", color=colors[0])
        plt.text(-1.0, 0.5, "AB2", color=colors[1])
        plt.text(-0.5, 0.45, "AB3", color=colors[2])
        plt.text(-.25, 0.35, "AB4", color=colors[3])
        plt.text(-.15, 0.2, "AB5", color=colors[4])
        plt.text(0.02, 0.05, "AB6", color=colors[5])
        
        plt.tight_layout()
        plt.savefig("img/adams_bashforth_stability.png")

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
    plt.savefig(title + ".png")

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
    plt.savefig("img/multistep_family_stability.png")
    plt.show()
    
if __name__ == "__main__":
    # stability_of_centered_diff_in_convection_diffusion_eq()
    # AB(False)
    # AB(True)
    # AM(False)
    # AM(True)
    # AM(False, True)
    custom_scheme_stability()
    plt.show()