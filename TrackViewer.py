'''
Author: Thomas Schiller
University: University of Central Florida
Institute: Institute for Simulation and Training
'''

import csv
import numpy as np
import matplotlib as plt

colorcode_forrest = [191, 242, 128, 255]
colorcode_sand = [253, 251, 239, 255]
colorcode_road = [160, 160, 160, 255]
#colorcode_water = [216, 31, 42, 255]

track_path = 'path_tracking/'
map_file = 'maps/Map01_TankSimEnv.csv'

# open the map file
with open(map_file, newline='') as csvfile_map:
    list_map = list(csv.reader(csvfile_map, delimiter=';'))

# open the tracking files
#with open(track_path, newline='') as csvfile_map:
#    self.list_map = list(csv.reader(csvfile_map, delimiter=';'))

# print the map with MatPlotLib
for y in range(64):
    for x in range(64):
        if list_map == 90:
            list_map[y][x] = colorcode_forrest
        if list_map == 91:
            list_map[y][x] = colorcode_sand
        if list_map == 92:
            list_map[y][x] = colorcode_road

arr_map = np.asarray(list_map)

