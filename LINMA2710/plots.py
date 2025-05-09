import matplotlib.pyplot as plt
import numpy as np

def finite_differences():
    t_max = 10
    z_max = 5
    num_t = 15
    num_z = 10

    t = np.linspace(0, t_max, num_t)
    z = np.linspace(0, z_max, num_z)
    Z, T = np.meshgrid(z, t)

    fig, ax = plt.subplots()

    for i in range(num_t):
        ax.plot([t[i]] * num_z, z, 'k--', lw=0.5, color="grey")  # Vertical lines
    for j in range(num_z):
        ax.plot(t, [z[j]] * num_t, 'k--', lw=0.5, color="grey")  # Horizontal lines
    ax.scatter(t[8], z[6], color="blue")
    ax.text(t[8] + 0.2, z[6], r'$u(t_n, x_j) = u_j^n$', color="blue")

    ax.annotate(text=r'$\Delta t$', xy=(t[5], z[4]), xytext=(t[5], z[5] + 0.09),
                arrowprops=dict(arrowstyle='<->', shrinkA=0, shrinkB=0),
                va='center', ha='center')

    ax.annotate(text=r'$\Delta x$', xy=(t[5], z[4]), xytext=(t[6] + 0.1, z[4]),
                arrowprops=dict(arrowstyle='<->', shrinkA=0, shrinkB=0),
                va='center', ha='center')

    ax.set_xlim(0, t_max)
    ax.set_ylim(0, z_max)
    ax.axis("equal")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("img/finite_diff.pdf")
    plt.show()

def refinement():
    fig, ax = plt.subplots()

    x = np.linspace(0, 3.99, 100)
    y = 1/(4-x)-0.25
    ax.plot(x, y, 'b-', lw=1)

    ax.set_xlabel(r'$\Delta x$')
    ax.set_ylabel(r'$\Delta t$')

    ax.quiver(6, 0, 0, 1, angles='xy', scale_units='xy', scale=0.1, color='black', label='h')

    idx = 4*len(x)//5
    arrow = x[idx+1], y[idx+1], -x[idx+1] + x[idx], -y[idx+1] + y[idx]

    ax.arrow(*arrow, shape='full', lw=0, length_includes_head=True, head_width=0.30, color='b')

    ax.text(4, 6, "Refinement path", color="blue")
    ax.text(5.7, 9.5, r"$h$")

    ax2 = ax.twinx()
    ax2.set_yticks([0])  
    ax.set_yticks([])
    ax.set_xticks([])

    ax.set_xlim(0, 6.1)
    ax.set_ylim(0, 10)
    plt.savefig("img/refinement.pdf")
    plt.show()


def FTCS():
    t_max = 5
    z_max = 5
    num_t = 5
    num_z = 5

    t = np.linspace(0, t_max, num_t)
    z = np.linspace(0, z_max, num_z)
    Z, T = np.meshgrid(z, t)

    fig, ax = plt.subplots()

    for i in range(num_t):
        ax.plot([t[i]] * num_z, z, '--', lw=0.5, color="grey")  # Vertical lines
    for j in range(num_z):
        ax.plot(t, [z[j]] * num_t, '--', lw=0.5, color="grey")  # Horizontal lines
    ax.scatter(t[2], z[2], color="blue")
    ax.scatter(t[3], z[2], color="blue")
    ax.scatter(t[1], z[2], color="blue")
    ax.scatter(t[2], z[3], color="blue")
    ax.text(t[2], z[2]+0.1, r'$u(t_n, x_j) = u_j^n$', color="blue", size=15)

    ax.set_xticks([t[2]], [r"$x_j$"], size=20)
    ax.set_yticks([z[2]], [r"$t_n$"], size=20)
    ax.set_xlim(0, t_max)
    ax.set_ylim(0, z_max)
    plt.tight_layout()
    plt.savefig("img/FTCS.pdf")
    plt.show()

def BTCS():
    t_max = 5
    z_max = 5
    num_t = 5
    num_z = 5

    t = np.linspace(0, t_max, num_t)
    z = np.linspace(0, z_max, num_z)
    Z, T = np.meshgrid(z, t)

    fig, ax = plt.subplots()

    for i in range(num_t):
        ax.plot([t[i]] * num_z, z, '--', lw=0.5, color="grey")  # Vertical lines
    for j in range(num_z):
        ax.plot(t, [z[j]] * num_t, '--', lw=0.5, color="grey")  # Horizontal lines
    ax.scatter(t[2], z[2], color="blue")
    ax.scatter(t[3], z[3], color="blue")
    ax.scatter(t[1], z[3], color="blue")
    ax.scatter(t[2], z[3], color="blue")
    ax.text(t[2], z[2]+0.1, r'$u(t_n, x_j) = u_j^n$', color="blue", size=15)

    ax.set_xticks([t[2]], [r"$x_j$"], size=20)
    ax.set_yticks([z[2]], [r"$t_n$"], size=20)
    ax.set_xlim(0, t_max)
    ax.set_ylim(0, z_max)
    plt.tight_layout()
    plt.savefig("img/BTCS.pdf")
    plt.show()

def CN():
    t_max = 5
    z_max = 5
    num_t = 5
    num_z = 5

    t = np.linspace(0, t_max, num_t)
    z = np.linspace(0, z_max, num_z)
    Z, T = np.meshgrid(z, t)

    fig, ax = plt.subplots()

    for i in range(num_t):
        ax.plot([t[i]] * num_z, z, '--', lw=0.5, color="grey")  # Vertical lines
    for j in range(num_z):
        ax.plot(t, [z[j]] * num_t, '--', lw=0.5, color="grey")  # Horizontal lines
    ax.scatter(t[1], z[2], color="blue")
    ax.scatter(t[2], z[2], color="blue")
    ax.scatter(t[3], z[2], color="blue")
    ax.scatter(t[1], z[3], color="blue")
    ax.scatter(t[2], z[3], color="blue")
    ax.scatter(t[3], z[3], color="blue")
    ax.text(t[2], z[2]+0.1, r'$u(t_n, x_j) = u_j^n$', color="blue", size=15)

    ax.set_xticks([t[2]], [r"$x_j$"], size=20)
    ax.set_yticks([z[2]], [r"$t_n$"], size=20)
    ax.set_xlim(0, t_max)
    ax.set_ylim(0, z_max)
    plt.tight_layout()
    plt.savefig("img/CN.pdf")
    plt.show()

def Dufort_frankel():
    t_max = 5
    z_max = 5
    num_t = 5
    num_z = 5

    t = np.linspace(0, t_max, num_t)
    z = np.linspace(0, z_max, num_z)
    Z, T = np.meshgrid(z, t)

    fig, ax = plt.subplots()

    for i in range(num_t):
        ax.plot([t[i]] * num_z, z, '--', lw=0.5, color="grey")  # Vertical lines
    for j in range(num_z):
        ax.plot(t, [z[j]] * num_t, '--', lw=0.5, color="grey")  # Horizontal lines
    ax.scatter(t[1], z[2], color="blue")
    ax.scatter(t[3], z[2], color="blue")
    ax.scatter(t[2], z[2], color="red")
    ax.scatter(t[2], z[3], color="blue")
    ax.scatter(t[2], z[1], color="blue")
    ax.text(t[2], z[2]+0.1, r'$u(t_n, x_j) = u_j^n$', color="red", size=15)

    ax.set_xticks([t[2]], [r"$x_j$"], size=20)
    ax.set_yticks([z[2]], [r"$t_n$"], size=20)
    ax.set_xlim(0, t_max)
    ax.set_ylim(0, z_max)
    plt.tight_layout()
    plt.savefig("img/DF.pdf")
    plt.show()

# finite_differences()
# refinement()
# FTCS()
# BTCS()
# CN()
Dufort_frankel()