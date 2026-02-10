# Retry: plotting ΔU(x) and F(x) with the same logic.

import numpy as np
import matplotlib.pyplot as plt

L = 1.0
l0 = 0.9
B = 100

def chord(theta):
    return (2 * L / theta) * np.sin(theta / 2)

def find_theta0(l0):
    a, b = 1e-6, np.pi - 1e-6
    for _ in range(100):
        m = 0.5 * (a + b)
        if chord(m) > l0:
            a = m
        else:
            b = m
    return 0.5 * (a + b)

theta0 = find_theta0(l0)

def s(theta):
    return (L / theta) * (1 - np.cos(theta / 2))

def h(theta):
    l = chord(theta)
    return 0.5 * np.sqrt(l0**2 - l**2)

def x(theta):
    return s(theta) + h(theta)

def delta_U(theta):
    return (B / (2 * L)) * (theta**2 - theta0**2)

thetas = np.linspace(theta0 + 1e-4, np.pi - 1e-4, 2000)

xs = x(thetas)
Us = delta_U(thetas)

dU_dtheta = np.gradient(Us, thetas)
dx_dtheta = np.gradient(xs, thetas)
Fs = dU_dtheta / dx_dtheta

order = np.argsort(xs)
xs = xs[order]
Us = Us[order]
Fs = Fs[order]

plt.figure()
plt.plot(xs, Us)
plt.xlabel("Draw distance x")
plt.ylabel("Delta U")
plt.title("Delta U vs Draw Distance")
plt.show()

plt.figure()
plt.plot(xs, Fs)
plt.xlabel("Draw distance x")
plt.ylabel("Force F")
plt.title("Force vs Draw Distance")
plt.show()
