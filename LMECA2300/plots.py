import matplotlib.pyplot as plt
import numpy as np
from scipy.special import j0, y0 


def phasor():
    omega_0 = 5
    omega = 10 

    fig, ax = plt.subplots()


    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)


    ax.arrow(-omega_0, 0, 0, 1, head_width=0.2, head_length=0.2, fc='blue', ec='blue')
    ax.arrow(omega_0, 0, 0, 1, head_width=0.2, head_length=0.2, fc='blue', ec='blue')

    ax.set_xlim(-2 * omega, 2 * omega)
    ax.set_ylim(-0.2, 2)
    ax.set_xticks([-omega_0, 0, omega_0])
    ax.set_xticklabels([r'$-\omega_0$', '0', r'$\omega_0$', ])
    ax.set_yticks([])
    plt.savefig("img/phasor.png")
    plt.show()

def bessel():
    x = np.linspace(0.01, 30, 200)
    plt.plot(x, j0(x), label=r"$J_0(x)$", color="blue")
    plt.plot(x, y0(x), label=r"$Y_0(x)$", color="lightgreen")
    plt.legend()
    plt.grid()
    plt.xlabel(r"$\rho$")
    plt.title("Bessel functions")
    plt.savefig("img/bessel.png")
    plt.show()


if __name__ == "__main__":
    # phasor()
    bessel()