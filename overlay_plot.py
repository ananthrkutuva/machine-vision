from pyproj import Proj
import pandas as pd
import matplotlib.pyplot as plt

# Make a dataframe from the GoPro GPS Data
df = pd.read_csv("data/gpsdata.csv")

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
x_list = []
y_list = []

# Loop through each of the latitude and longitude values and append to the lists
for lat, lon in zip(latitude_list, longitude_list):
    x_new, y_new = p(lon, lat)
    x_list.append(x_new - 313462.56)
    y_list.append(y_new - 4684648.4)

# print(x_list)
# print(y_list)

# Set the initial and final x and y coordinates to be plotted
init_x = x_list[0]
init_y = y_list[0]
final_x = x_list[-1]
final_y = y_list[-1]

# Plot everything
plt.plot(x_list, y_list)
plt.scatter(init_x, init_y, c="green")
plt.scatter(final_x, final_y, c="red")
plt.xlabel("X Distance (m)")
plt.ylabel("Y Distance (m)")
plt.title("Plot of Bicycle Position")
plt.show()
plt.close()