from pyproj import Proj
import pandas as pd
import matplotlib.pyplot as plt

# Make a dataframe from the GoPro GPS Data
df = pd.read_csv("data/olin.csv")

# Take out the relevant data from the CSV File
relevant_data = df[["date", "GPS (Lat.) [deg]", "GPS (Long.) [deg]"]]

# Separate the data into individual lists
date_list = df["date"].to_list()
latitude_list = df["GPS (Lat.) [deg]"].to_list()
longitude_list = df["GPS (Long.) [deg]"].to_list()

# print(date_list)
# print(latitude_list)
# print(longitude_list)

# Setup a projection using the pyproj library (lat long to meters)
p = Proj(proj='utm',zone=19, ellps='WGS84', preserve_units=False)

# Allocate x and y coordinates
x_list_projected = []
y_list_projected = []

# Loop through each of the latitude and longitude values and append to the lists
for lat, lon in zip(latitude_list, longitude_list):
    x_new, y_new = p(lon, lat)
    x_list_projected.append(x_new)
    y_list_projected.append(y_new)

# Record the maximum value in both the x and y lists
max_x_value = max(x_list_projected)
max_y_value = max(y_list_projected)

# The final value in the list is how much to shift the graph over by
x_shift = x_list_projected[-1]
y_shift = y_list_projected[-1]

# Allocate space for the shifted list
x_list_final = []
y_list_final = []

# Shift all values
for x, y in zip(x_list_projected, y_list_projected):
    x_list_final.append(x - x_shift)
    y_list_final.append(y - y_shift)

# Record the initial and final x and y coordinates
init_x = x_list_final[0]
init_y = y_list_final[0]
final_x = x_list_final[-1]
final_y = y_list_final[-1]

# Plot everything
plt.plot(x_list_final, y_list_final)
plt.scatter(init_x, init_y, c="green")
plt.scatter(final_x, final_y, c="red")
plt.xlabel("X Distance (m)")
plt.ylabel("Y Distance (m)")
plt.title("Plot of Bicycle Position")
plt.show()
plt.close()