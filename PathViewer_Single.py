'''
Author: Thomas Schiller
University: University of Central Florida
Institute: Institute for Simulation and Training

This file is a viewer for a single path.
Set the map and path file at the beginning after the imports.
'''

from matplotlib import pyplot as plt
import numpy as np
import csv
from PIL import Image

# set image file
map_file = 'maps/Map01_TankSimEnv.csv'
scenar_file = 'scenars/Scenar01_TankSimEnv.csv'
path_file = 'path_tracking/Path_1654526306.731136.csv'

# set the color codes
colorcode_forrest = np.array([191, 242, 128])
colorcode_sand = np.array([253, 251, 239])
colorcode_road = np.array([160, 160, 160])
colorcode_goal = np.array([153, 8, 0])
colorcode_tank = np.array([119, 227, 242])

# load map from csv file
image_data = np.genfromtxt(map_file, delimiter=';')

rgb_image = np.zeros([64,64,3], dtype=np.uint8)

for y in range(64):
    for x in range(64):
        if image_data[x,y] == 90:
            rgb_image[x,y] = colorcode_forrest
        if image_data[x,y] == 91:
            rgb_image[x,y] = colorcode_sand
        if image_data[x,y] == 92:
            rgb_image[x,y] = colorcode_road


# load scenar file from csv
with open(scenar_file, newline='') as csvfile_scenar:
    list_scenar = list(csv.reader(csvfile_scenar, delimiter=';'))

print(list_scenar)

# grab the coordinates for the goal (flag) and tank or drone
for y in range(64):
    for x in range(64):
        if list_scenar[y][x] == "99":
            rgb_image[y,x] = colorcode_goal
            goal_coord_x = x
            goal_coord_y = y
        elif list_scenar[y][x] == "10":
            rgb_image[y, x] = colorcode_tank
            tank_coord_x = x
            tank_coord_y = y
        pass

# save the map as png file in the path tracking folder; it will be used to plot the graph
im = Image.fromarray(rgb_image)
im.save("path_tracking/map_image.png")

# for debugging
#print(np.shape(rgb_image))
#print(rgb_image)

# load the path tracking file
with open(path_file, newline='') as csvfile_map:
    list_path = list(csv.reader(csvfile_map, delimiter=','))

# remove the first line from the loaded csv file
list_path.remove(['x', 'y'])

# divide the loaded csv file into the x and y coordinates
list_path_x = []
list_path_y = []
for i in range(len(list_path)):
    list_path_x.append(int(list_path[i][0]))
    list_path_y.append(int(list_path[i][1]))

# Sketch the Path with the map as a background
fig = plt.figure()
ax = fig.subplots()

ax.plot(list_path_x, list_path_y, color="r")
img = plt.imread("path_tracking/map_image.png")
ax.imshow(img)

major_ticks = np.arange(0, 65, 16)
ax.set_xticks(major_ticks)
ax.set_yticks(major_ticks)
ax.grid(which='major', alpha=0.5)

plt.title(f"Map: {map_file}\nPath:{path_file}")

plt.show()