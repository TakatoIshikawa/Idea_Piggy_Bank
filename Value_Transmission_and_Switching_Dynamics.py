import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# Parameter settings: grid size, time step, etc.
nx, ny = 50, 50       # Size of the 2D grid
dx = 1.0              # Spatial step
dt = 0.1              # Time step
total_steps = 1000    # Total number of simulation steps

D_a = 0.1  # Diffusion coefficient for A
D_b = 0.1  # Diffusion coefficient for B
alpha = 0.1  # Strength of parental influence
beta = 0.7   # Strength of switching term
delta = 2.0  # Threshold parameter
k_sig = 5.0  # Steepness of sigmoid function (switching term)

max_strength = 10.0  # Maximum parental influence
k = 0.02  # Steepness of sigmoid for parental influence growth

# Initialization: Place children of type A on the left, and B on the right
C_a = np.zeros((nx, ny))
C_b = np.zeros((nx, ny))

# Initial condition: left half (i < nx//2) set C_a = 1, right half set C_b = 1
C_a[:, :nx//2] = 1.0
C_b[:, nx//2:] = 1.0

# Define parental type masks (fixed in space): left side influenced by parent A, right by parent B
# Cells influenced by parent A have A_force = 1; those by parent B have B_force = 1
A_mask = np.zeros((nx, ny))
B_mask = np.zeros((nx, ny))
A_mask[:, :nx//2] = 1.0  # Left region influenced by parent A
B_mask[:, nx//2:] = 1.0  # Right region influenced by parent B

# Definition of sigmoid function (used for switching term)
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-k_sig * x))

# Laplacian on a 2D grid (finite difference method with periodic boundary conditions)
def laplacian(Z):
    # Using periodic boundary conditions with np.roll
    Ztop = np.roll(Z, 1, axis=0)
    Zbot = np.roll(Z, -1, axis=0)
    Zleft = np.roll(Z, 1, axis=1)
    Zright = np.roll(Z, -1, axis=1)
    return (Ztop + Zbot + Zleft + Zright - 4 * Z) / (dx**2)

# Sigmoid growth for bounded parental influence
def bounded_influence(t):
    return max_strength * (1.0 / (1.0 + np.exp(-k * (t - 100))))

# Update function for time evolution
def update(frame):
    global C_a, C_b

    # Current time (increases by dt each frame)
    t = frame * dt

    # Parental influence increases with time: strength of parent A and B = t
    # Each cell is influenced by its corresponding parent via A_mask and B_mask
    parent_strength = bounded_influence(t)
    A_force = A_mask * parent_strength
    B_force = B_mask * parent_strength

    # Compute switching term
    # ∆ = |C_a - C_b| - δ
    diff = np.abs(C_a - C_b) - delta
    # Switching rates a→b and b→a (using sigmoid for smooth transitions)
    theta_a_to_b = beta * C_a * sigmoid(diff)
    theta_b_to_a = beta * C_b * sigmoid(diff)

    # Diffusion term (Laplacian)
    lap_A = laplacian(C_a)
    lap_B = laplacian(C_b)

    # Time evolution (Euler method)
    # Parental influence term: α*(parental_strength - current_value)
    dC_a = D_a * lap_A + alpha * (A_force - C_a) - theta_a_to_b
    dC_b = D_b * lap_B + alpha * (B_force - C_b) - theta_b_to_a

    # Update concentrations
    C_a = C_a + dt * dC_a
    C_b = C_b + dt * dC_b

    # Update plots: use color to represent difference (C_a - C_b)
    im1.set_array(C_a)
    im2.set_array(C_b)
    im3.set_array(C_a - C_b)
    ax1.title.set_text(f'C_a at t={t:.2f}')
    ax2.title.set_text(f'C_b at t={t:.2f}')
    ax3.title.set_text(f'C_a - C_b at t={t:.2f}')
    return im1, im2, im3

# Prepare plots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
im1 = ax1.imshow(C_a, cmap="Reds", vmin=-1, vmax=5)
im2 = ax2.imshow(C_b, cmap="Blues", vmin=-1, vmax=5)
im3 = ax3.imshow(C_a - C_b, cmap="bwr", vmin=-3, vmax=3)
plt.tight_layout()

# Create animation
anim = animation.FuncAnimation(fig, update, frames=total_steps, interval=50, blit=False)

plt.show()

