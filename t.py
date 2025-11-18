import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

x = np.linspace(0.1, 10, 100) 
t = np.linspace(0, 10, 100)

X, T = np.meshgrid(x, t)
S = 0.5 * (X - 1/X - T + np.sqrt((X - 1/X - T)**2 + 4))
U = (S**2 / (S**2 + 1)) * ((X**2 + 1) / X**2) * np.exp(-S)

fig = plt.figure(figsize=(11, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, T, U, alpha=0.8, color="tan", label="Surface")

# --- Lignes iso ---
t_integers = np.arange(int(t.min()), int(t.max())+1)
iso_lines = []
for ti in t_integers:
    Si = 0.5 * (x - 1/x - ti + np.sqrt((x - 1/x - ti)**2 + 4))
    Ui = (Si**2 / (Si**2 + 1)) * ((x**2 + 1) / x**2) * np.exp(-Si)
    line, = ax.plot(x, ti*np.ones_like(x), Ui, color='red', linewidth=1.2)
    iso_lines.append(line)

# --- Caractéristiques ---
s = np.arange(-2.01, 10, 1)
char_lines = []
for si in s:
    ti = (1-si**2)/si + x - 1/x
    mask = ti >= 0
    line, = ax.plot(x[mask], ti[mask], np.zeros_like(x[mask]), color='limegreen')
    char_lines.append(line)
line, = ax.plot(np.zeros(100), t, 0, color='limegreen')
char_lines.append(line)

# --- Courbe Gamma ---
gamma_line, = ax.plot(x, np.zeros(100), 0, color='darkblue')

ax.set_xlabel(r'$x/L$')
ax.set_ylabel(r'$c_0t/L$')
ax.set_zlabel(r'$u/u_0$')

# --- Boutons ---
rax = plt.axes([0.82, 0.4, 0.15, 0.2])
labels = ["Surface", "Lignes iso", "Caractéristiques", r'$\Gamma$']
visibility = [True, True, True, True]
check = CheckButtons(rax, labels, visibility)

# Colors for each label
colors = {
    "Surface": "tan",
    "Lignes iso": "red",
    "Caractéristiques": "limegreen",
    r"$\Gamma$": "darkblue"
}

# Style the checkboxes
for rect, label in zip(check.rectangles, check.labels):
    rect.set_facecolor("lightgray")   # background
    rect.set_alpha(0.3)
    label.set_fontsize(11)
    text = label.get_text()
    if text in colors:
        label.set_color(colors[text])  # text color = line color

def toggle(label):
    if label == "Surface":
        surf.set_visible(not surf.get_visible())
    elif label == "Lignes iso":
        for l in iso_lines: l.set_visible(not l.get_visible())
    elif label == "Caractéristiques":
        for l in char_lines: l.set_visible(not l.get_visible())
    elif label == r"$\Gamma$":
        gamma_line.set_visible(not gamma_line.get_visible())
    plt.draw()

check.on_clicked(toggle)

plt.show()