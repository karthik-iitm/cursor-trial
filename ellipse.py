import matplotlib.pyplot as plt
import numpy as np

# Create the ellipse
t = np.linspace(0, 2*np.pi, 1000)
x = np.cos(t) / 2  # Divide by 2 because 4x^2 = 4 means x^2 = 1, so x ranges from -1/2 to 1/2
y = np.sin(t)

# Plot the ellipse
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', label='Ellipse: $4x^2 + y^2 = 4$')

# Plot the point (1, 0)
plt.plot(1, 0, 'go', markersize=10, label='(1, 0)')

# Plot the farthest points
farthest_x = -1/3
farthest_y = 4*np.sqrt(2)/3
plt.plot([farthest_x, farthest_x], [farthest_y, -farthest_y], 'ro', markersize=10, label='Farthest points')

# Add labels and title
plt.xlabel('x')
plt.ylabel('y')
plt.title('Ellipse $4x^2 + y^2 = 4$ and Farthest Points from (1, 0)')
plt.grid(True)
plt.legend()
plt.axis('equal')

# Set the x and y axis limits to show the full ellipse and the point (1,0)
plt.xlim(-0.75, 1.25)
plt.ylim(-1.25, 1.25)

# Save the figure
plt.savefig('ellipse_diagram.png', dpi=300, bbox_inches='tight')
plt.close()
