# Modified diffusion equation
from matplotlib import pyplot
import itertools
import scipy

alpha = 0.03
beta = 0.2
gamma = 3.5

cmap = pyplot.cm.viridis  # good for color blindness


# Plot traces of how opinion and weight change over time
for o1, weight, o2 in [
    [0.25, 0.95,0], [0.45, 0.95,0], [0.55, 0.95,0], [0.65, 0.95,0], [0.75, 0.95,0],
    [0.85, 0.95,0], [0.95, 0.95,0], [0.95, 0.95,0.25], [0.95, 0.95,0.45], [0.95, 0.95,0.65],
    [0.95, 0.95,0.95],[0.95, 0.45,0.95], [0.7,0.95,0.7], [0.8,0.95,0.6], [0.25,0.5,0.25]
]:
    ow = [[0.0, 0.0, weight, o1, o2]]
    new_weight=1
    for i in range(200):
        if new_weight==0:
            break
        delta_o1 = alpha * ow[-1][2] * (ow[-1][0] - ow[-1][3])
        delta_o2 = alpha * ow[-1][2] * (ow[-1][1] - ow[-1][4])
        delta_w = (
            beta * ow[-1][2] * (1-ow[-1][2]) *
            (1-gamma*(abs(ow[-1][3] - ow[-1][0])+abs(ow[-1][4] - ow[-1][1]))))
        new_weight = ow[-1][2] + delta_w
        if new_weight < 0.05:
            new_weight = 0
        ow.append([ow[-1][0] - delta_o1, ow[-1][1] - delta_o2, new_weight, ow[-1][3] + delta_o1, ow[-1][4] + delta_o2])
    pyplot.plot(
        [abs(row[0] - row[3])+abs(row[1] - row[4]) for row in ow],
        [row[2] for row in ow],
        color=(cmap(0.15) if ow[-1][2] == 0 else cmap(0.75)),
        alpha=0.75)

# Plot vector field
d = scipy.linspace(0, 2, 9)  # the difference in opinion, |o_i - o_j|
weight = scipy.linspace(0, 1, 6)   # the edge weight, w_ij
ow_grid = scipy.meshgrid(d, weight)
delta_o_grid = -2.4*alpha * ow_grid[1] * ow_grid[0]
delta_w_grid = beta * ow_grid[1] * (1-ow_grid[1]) * (1 - gamma * ow_grid[0])
pyplot.quiver(ow_grid[0], ow_grid[1], delta_o_grid, delta_w_grid)
#
# # Annotate plot
pyplot.xlabel('|o_i1-o_j1|+|o_i2-o_j2|')
pyplot.ylabel('weight')
pyplot.plot([0, 2], [0.05, 0.05], 'k--')
pyplot.show()