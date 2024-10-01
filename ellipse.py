import matplotlib.pyplot as plt
import numpy as np

# Create the ellipse
t = np.linspace(0, 2*np.pi, 1000)
x = np.cos(t)  # x ranges from -1 to 1
y = 2 * np.sin(t)  # y ranges from -2 to 2

# Create the plot
plt.figure(figsize=(8, 8))  # Adjusted figure size for better text-width fit
plt.plot(x, y, 'b-', label='Ellipse: 4x² + y² = 4')

# Plot the point (1, 0)
plt.plot(1, 0, 'go', markersize=10, label='Point (1, 0)')
plt.annotate('(1, 0)', xy=(1, 0), xytext=(1.05, 0.1), fontsize=9)

# Plot the farthest points
farthest_x = -1/3
farthest_y = 4*np.sqrt(2)/3
plt.plot([farthest_x], [farthest_y], 'ro', markersize=10)
plt.plot([farthest_x], [-farthest_y], 'ro', markersize=10, label='Farthest points')
plt.annotate(f'(-1/3, 4√2/3)', xy=(farthest_x, farthest_y), xytext=(farthest_x-0.4, farthest_y+0.1), fontsize=9)
plt.annotate(f'(-1/3, -4√2/3)', xy=(farthest_x, -farthest_y), xytext=(farthest_x-0.4, -farthest_y-0.2), fontsize=9)

# Draw lines from (1,0) to farthest points
plt.plot([1, farthest_x], [0, farthest_y], 'r--', alpha=0.5)
plt.plot([1, farthest_x], [0, -farthest_y], 'r--', alpha=0.5)

# Add labels and title
plt.xlabel('x')
plt.ylabel('y')
plt.title('Ellipse $4x^2 + y^2 = 4$ and Farthest Points from (1, 0)')
plt.grid(True)
plt.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize=8)  # Adjusted legend position and font size

# Use tight_layout to ensure all elements fit
plt.tight_layout()

# Adjust the axis limits
plt.xlim(-1.25, 1.25)
plt.ylim(-2.25, 2.25)

# Save the figure
plt.savefig('ellipse_problem.png', dpi=300, bbox_inches='tight')
plt.close()
