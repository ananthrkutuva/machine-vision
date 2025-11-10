from pyproj import Proj
import pandas as pd
import matplotlib.pyplot as plt
import math

df = pd.read_csv("data/gpsdata.csv")

relevant_data = df[["date", "GPS (Lat.) [deg]", "GPS (Long.) [deg]"]]

date_list = df["date"].to_list()
latitude_list = df["GPS (Lat.) [deg]"].to_list()
longitude_list = df["GPS (Long.) [deg]"].to_list()

# print(date_list)
# print(latitude_list)
# print(longitude_list)

p = Proj(proj='utm',zone=19, ellps='WGS84', preserve_units=False)

x_list = []
y_list = []

for lat, lon in zip(latitude_list, longitude_list):
    x_new, y_new = p(lon, lat)
    x_list.append(x_new - 313462.56)
    y_list.append(y_new - 4684648.4)

print(x_list)
print(y_list)

init_x = x_list[0]
init_y = y_list[0]
final_x = x_list[-1]
final_y = y_list[-1]

plt.plot(x_list, y_list)
plt.scatter(init_x, init_y, c="green")
plt.scatter(final_x, final_y, c="red")
plt.xlabel("X Coordinates")
plt.ylabel("Y Coordinates")
plt.title("Plot of Bicycle Position")
plt.show()
plt.close()