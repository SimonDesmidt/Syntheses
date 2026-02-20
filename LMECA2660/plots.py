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

if __name__ == "__main__":
    stability_of_centered_diff_in_convection_diffusion_eq()
    plt.show()