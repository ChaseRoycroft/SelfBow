import numpy as np
import matplotlib.pyplot as plt

# =======================
# Bow parameters
# =======================
L = 1.0      # limb arc length [m]
l0 = 0.75    # bowstring length [m]
E = 1e10     # Young's modulus [Pa]
r = 0.01     # radius of circular cross-section [m]
#NOTE: Currently, the bow is much too powerful because I'm assuming a fixed circular radius along the length of the bow limb, whereas real bows taper (and more commonly use rectangular cross-sections, although I've set r to take that part into account).

# Arrow parameters
m_arrow = 0.02  # mass [kg]
theta_deg = 45  # launch angle in degrees

g = 9.81  # gravity [m/s²]

# =======================
# Bending stiffness
# =======================
I = (np.pi/4) * r**4
B = E * I

# =======================
# Circular-arc formulas
# =======================
def l_of_a(a):
    return L * np.sin(a)/a

def d_of_a(a):
    l = l_of_a(a)
    return 0.5 * np.sqrt(l0**2 - l**2)

def U_of_a(a):
    return 2 * B * a**2 / L

def F_of_a(a):
    l = l_of_a(a)
    dl_da = L * (a*np.cos(a) - np.sin(a)) / a**2
    d = d_of_a(a)
    ddd_a = - l * dl_da / (2*d)
    dU_da = 4*B*a / L
    F = dU_da / ddd_a
    return F

# =======================
# Generate curves
# =======================
a_vals = np.linspace(0.01, 2.5, 1000)
#NOTE: np.pi is the maximum value for a that's geometrically possible.

d_vals = np.array([d_of_a(a) for a in a_vals])
F_vals = np.array([F_of_a(a) for a in a_vals])
U_vals = np.array([U_of_a(a) for a in a_vals])

# =======================
# Compute firing velocity and range
# =======================
v_vals = np.sqrt(2*U_vals/m_arrow)
theta_rad = np.radians(theta_deg)
R_vals = v_vals**2 * np.sin(2*theta_rad)/g

# =======================
# Plot F vs d
# =======================
plt.figure(figsize=(8,5))
plt.plot(d_vals, F_vals/1e2, label="Draw force (N)")
plt.xlabel("Draw distance d [m]")
plt.ylabel("Draw force F [N]")
plt.title("Self-bow: Draw force vs Draw distance")
plt.grid(True)
plt.legend()
plt.show()

# =======================
# Plot U vs d
# =======================
plt.figure(figsize=(8,5))
plt.plot(d_vals, U_vals, label="Elastic energy U")
plt.xlabel("Draw distance d [m]")
plt.ylabel("Stored energy U [J]")
plt.title("Self-bow: Elastic energy vs Draw distance")
plt.grid(True)
plt.legend()
plt.show()

# =======================
# Plot nominal range vs draw distance
# =======================
plt.figure(figsize=(8,5))
plt.plot(d_vals, R_vals, color='green', label=f"Nominal range ({theta_deg}° launch)")
plt.xlabel("Draw distance d [m]")
plt.ylabel("Nominal range R [m]")
plt.title("Self-bow: Nominal arrow range vs Draw distance")
plt.grid(True)
plt.legend()
plt.show()
