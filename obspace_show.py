'''
Author: Thomas Schiller
University: University of Central Florida
Institute: Institute for Simulation and Training
'''



import csv
import os
import time

from colorama import Fore, Back, Style

map_file = 'observation_space/observation_space.csv'

# set the reduced observation space
reduced_obspace = True
reduced_obspace_size = 25  # 5 x 5
#reduced_obspace_size = 49  # 7 x 7


finished = False

if reduced_obspace:
    if reduced_obspace_size == 25:
        obspace_length = 5
    if reduced_obspace_size == 49:
        obspace_length = 7
else:
    obspace_length = 64

while not finished:

    time.sleep(0.1)

    # load observation space file
    with open(map_file, newline='') as csvfile_obspace:
        list_obspace = list(csv.reader(csvfile_obspace, delimiter=';'))

    # convert map list to int
    for y in range(obspace_length + 1):
        for x in range(obspace_length):
            list_obspace[y][x] = int(list_obspace[y][x])

    # clear screen for rendering new frame of the map
    os.system('clear')

    # render the observation space in terminal
    print(Back.BLACK + Fore.YELLOW, "Distance to Goal: ", list_obspace[obspace_length][0], end="\n" + Back.BLACK)
    #print(Back.BLACK + Fore.YELLOW, "Angle to Goal: ", list_obspace[obspace_length][1], end="\n" + Back.BLACK)
    if list_obspace[obspace_length][1] == 1:
        print(Back.BLACK + Fore.YELLOW, "Direction to Goal: ", "North", end="\n" + Back.BLACK)
    elif list_obspace[obspace_length][1] == 2:
        print(Back.BLACK + Fore.YELLOW, "Direction to Goal: ", "East", end="\n" + Back.BLACK)
    elif list_obspace[obspace_length][1] == 3:
        print(Back.BLACK + Fore.YELLOW, "Direction to Goal: ", "South", end="\n" + Back.BLACK)
    elif list_obspace[obspace_length][1] == 4:
        print(Back.BLACK + Fore.YELLOW, "Direction to Goal: ", "West", end="\n" + Back.BLACK)
    #elif list_obspace[obspace_length][0] == 4:
    #    print(Back.BLACK + Fore.YELLOW, "Direction to Goal: ", "Not defined", end="\n" + Back.BLACK)
    print()

    for y in range(obspace_length):
        for x in range(obspace_length):
            if list_obspace[y][x] == 90:
                print(Back.GREEN + '  ', end=" " + Back.BLACK)
            elif list_obspace[y][x] == 92:
                print(Back.WHITE + '  ', end=" " + Back.BLACK)
            elif list_obspace[y][x] == 91:
                print(Back.YELLOW + '  ', end=" " + Back.BLACK)
            elif list_obspace[y][x] == 93:
                print(Back.BLUE + '  ', end=" " + Back.BLACK)
            elif list_obspace[y][x] == 99:
                print(Back.MAGENTA + ' G', end=" " + Back.BLACK)
            elif list_obspace[y][x] == 10:
                print(Back.CYAN + Fore.BLACK + ' T', end=" " + Back.BLACK)
            elif list_obspace[y][x] == 11:
                print(Back.BLACK + '  ', end=" " + Back.BLACK)
        print("")

        #print(f"Distance to Goal: {list_obspace[obspace_length + 1][1]}")
        #print("")
            #elif list_obspace[y][x] == 80:
            #            print(Back.RED + ' B', end=" " + Back.BLACK)

