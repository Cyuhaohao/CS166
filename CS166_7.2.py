import numpy as np
import matplotlib.pyplot as plt
x = y = np.array([-2, -1, 0, 1, 2])
x_grid, y_grid = np.meshgrid(x, y)


vector_x = x_grid + y_grid
vector_y = x_grid - y_grid

plt.figure(figsize=(6, 6))
plt.quiver(x_grid, y_grid, vector_x, vector_y)
plt.xlim(-2.5, 2.5)
plt.ylim(-2.5, 2.5)
plt.show()