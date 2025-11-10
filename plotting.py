import matplotlib.pyplot as plt

x_coords = [1, 2, 3, 4, 5]
y_coords = [1, 2, 3, 4, 5]

init_x = x_coords[0]
init_y = y_coords[0]
final_x = x_coords[-1]
final_y = y_coords[-1]

plt.plot(x_coords, y_coords)
plt.scatter(init_x, init_y, c="green")
plt.scatter(final_x, final_y, c="red")
plt.xlabel("X Coordinates")
plt.ylabel("Y Coordinates")
plt.title("Plot of Bicycle Position")
plt.show()