import numpy as np
import matplotlib.pyplot as plt

# Constants
rho = 1.0  # Density of fluid (e.g., air)
U = 1.0    # Velocity of fluid relative to sphere
sphere_radius = 1.0  # Radius of the sphere
viscosity = 0.1  # Dynamic viscosity of the fluid

# Reynolds number calculation
Re = (rho * U * 2 * sphere_radius) / viscosity

# Drag coefficient calculation for a sphere (Stokes' drag)
if Re <= 0.1:
    Cd = 24 / Re
else:
    Cd = 0.44

# Display the results
print(f"Reynolds Number (Re): {Re}")
print(f"Drag Coefficient (Cd): {Cd}")

# Plot the drag coefficient as a function of Reynolds number
Re_values = np.linspace(0.1, 100, 1000)
Cd_values = np.zeros_like(Re_values)

for i, Re in enumerate(Re_values):
    if Re <= 0.1:
        Cd_values[i] = 24 / Re
    else:
        Cd_values[i] = 0.44

plt.figure()
plt.plot(Re_values, Cd_values)
plt.xlabel('Reynolds Number (Re)')
plt.ylabel('Drag Coefficient (Cd)')
plt.title('Drag Coefficient vs. Reynolds Number for a Sphere')
plt.grid(True)
plt.show()
