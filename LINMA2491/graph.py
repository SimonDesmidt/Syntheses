import numpy as np
import matplotlib.pyplot as plt

def graph():
    x = np.linspace(-1, 11, 200)
    y_functions = [7/3 - x, x - 7/3, (x + 1) / 3, (5 - x) / 3]

    points = [
        (0, 0, r"$x_1$"),
        (10, 7/3 - 10, r"$x_2$"),
        (7/3, 0, r"$x_3$"),
        (1.5, 5/6, r"$x_4$"),
        (2, 1, r"$x_5$")
    ]

    num_plots = 4 
    fig, axes = plt.subplots(2, 2, figsize=(12, 10), sharex=True, sharey=True)
    axes = axes.flatten()

    for i in range(num_plots):
        ax = axes[i]

        for j in range(i + 1):
            ax.plot(x, y_functions[j], label=f"Cut {j + 1}") # Plot the cuts

        # Scatter points up to the i-th iteration
        for j in range(i + 2):
            x_point, y_point, label = points[j]
            ax.scatter(x_point, y_point, color='orange')
            ax.text(x_point + 0.2, y_point + 0.2, label, fontsize=14, ha='right')

        # Fill the area above all lines with a hatch pattern within the constraint 0 <= x <= 10
        y_max = np.maximum.reduce([y_functions[k] for k in range(i + 1)])
        ax.fill_between(x, y_max, 10, where=(x >= 0) & (x <= 10), color='gray', alpha=0.3, hatch='///', edgecolor='gray')

        ax.axhline(0, color='black', linewidth=0.8)
        ax.axvline(0, color='black', linewidth=0.8)
        ax.axvline(10, color='red', linestyle='--', linewidth=1.5)
        ax.axvline(0, color='red', linestyle='--', linewidth=1.5)

        ax.set_ylim(-10, 10)
        ax.legend()
        ax.set_title(f'Iteration {i + 1}')

    plt.tight_layout()
    plt.savefig("img/l_shaped_algo.pdf")
    plt.show()

graph()