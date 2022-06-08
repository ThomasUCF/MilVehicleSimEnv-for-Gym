'''
Author: Thomas Schiller
University: University of Central Florida
Institute: Institute for Simulation and Training

This Version has IED function included!
'''

import csv
import math
import os
import time
from gym import Env
from gym.spaces import Discrete, Box
from colorama import Fore, Back, Style
import merge_obspace


class ThesisSimEnv(Env):
    def __init__(self):
        # set Path Tracking
        self.path_tracking = True
        if self.path_tracking:
            self.path_track_x = []
            self.path_track_y = []

        # set Drone Mode
        self.drone_mode = False
        self.speed_drone = 1

        # Set episode length
        self.timesteps = 60
        self.episode_length = self.timesteps

        # set map size (needs to correlate with csv-file size!)
        self.map_length = 64

        # set terrain constraints
        self.speed_road = 3
        self.speed_sand = 2
        self.speed_forrest = 1

        # set Map and Scenar File!
        map_file = "../maps/Map01_TankSimEnv.csv"
        self.scenar_file = "../scenars/Scenar05_TankSimEnv.csv"

        # show IEDs to user in rendering
        self.show_ied = True

        self.ied_attack = False

        # load map file
        with open(map_file, newline='') as csvfile_map:
            self.list_map = list(csv.reader(csvfile_map, delimiter=';'))
        # convert map list to int
        for y in range(self.map_length):
            for x in range(self.map_length):
                self.list_map[y][x] = int(self.list_map[y][x])

        # load scenar file
        with open(self.scenar_file, newline='') as csvfile_scenar:
            self.list_scenar = list(csv.reader(csvfile_scenar, delimiter=';'))
        # convert scenar list to int
        for y in range(self.map_length):
            for x in range(self.map_length):
                self.list_scenar[y][x] = int(self.list_scenar[y][x])

        # grab the coordinates for the goal (flag)
        for y in range(self.map_length):
            for x in range(self.map_length):
                if self.list_scenar[y][x] == 99:
                    self.y_coord_goal = y
                    self.x_coord_goal = x
                    pass

        # grab the coordinates for the IED
        for y in range(self.map_length):
            for x in range(self.map_length):
                if self.list_scenar[y][x] == 80:
                    self.y_coord_ied = y
                    self.x_coord_ied = x
                    pass

        # Set the Action Space
        self.action_space = Discrete(9)

        # Set the Framework List for the Observation Space
        with open(map_file, newline='') as csvfile_observation_space:
            self.observation_space = list(csv.reader(csvfile_observation_space, delimiter=';'))
            for y in range(self.map_length):
                for x in range(self.map_length):
                    self.observation_space[y][x] = int(0)



    def step(self, action):
        # getting the coordination of the tank
        for y in range(self.map_length):
            for x in range(self.map_length):
                if self.list_scenar[y][x] == 10:
                    self.y_coord = y
                    self.x_coord = x
                    pass

        # track coordinates when Path Tracking is True
        if self.path_tracking:
            self.path_track_x.append(self.x_coord)
            self.path_track_y.append(self.y_coord)

        # checking on which terrain tank is and set according speed for this step
        if self.drone_mode:
            self.distance_move = self.speed_drone
        else:
            if self.list_map[self.y_coord][self.x_coord] == 92:
                self.distance_move = self.speed_road
            elif self.list_map[self.y_coord][self.x_coord] == 91:
                self.distance_move = self.speed_sand
            elif self.list_map[self.y_coord][self.x_coord] == 90:
                self.distance_move = self.speed_forrest

        # actual movement ...
        # move NORTH
        if action == 1:
            if self.y_coord > self.distance_move:

                # storing each coordinate of the path going for this one step
                # it will be used to check if IED attack applies
                if not self.drone_mode:
                    self.path_step_x = []
                    self.path_step_y = []
                    for m in range(1, self.distance_move + 1):
                        #self.path_step_x.append(self.list_scenar[x + m])
                        self.path_step_x.append(self.x_coord)
                        self.path_step_y.append(self.y_coord - m)

                # this is the actual move; it writes the new coordinate in the scenar list
                self.list_scenar[self.y_coord - self.distance_move][self.x_coord] = self.list_scenar[self.y_coord][self.x_coord]
                self.list_scenar[self.y_coord][self.x_coord] = 0



        # move NORTH-EAST
        elif action == 2:
            if (self.x_coord < self.map_length + self.distance_move) and (self.y_coord > self.distance_move):

                # storing each coordinate of the path going for this one step
                # it will be used to check if IED attack applies
                if not self.drone_mode:
                    self.path_step_x = []
                    self.path_step_y = []
                    for m in range(1, self.distance_move + 1):
                        #self.path_step_x.append(self.list_scenar[x + m])
                        self.path_step_x.append(self.x_coord + m)
                        self.path_step_y.append(self.y_coord - m)


                self.list_scenar[self.y_coord - self.distance_move][self.x_coord + self.distance_move] = self.list_scenar[self.y_coord][self.x_coord]
                self.list_scenar[self.y_coord][self.x_coord] = 0

        # move EAST
        elif action == 3:
            if self.x_coord < self.map_length + self.distance_move:

                # storing each coordinate of the path going for this one step
                # it will be used to check if IED attack applies
                if not self.drone_mode:
                    self.path_step_x = []
                    self.path_step_y = []
                    for m in range(1, self.distance_move + 1):
                        #self.path_step_x.append(self.list_scenar[x + m])
                        self.path_step_x.append(self.x_coord + m)
                        self.path_step_y.append(self.y_coord)

                self.list_scenar[self.y_coord][self.x_coord + self.distance_move] = self.list_scenar[self.y_coord][self.x_coord]
                self.list_scenar[self.y_coord][self.x_coord] = 0

        # move SOUTH-EAST
        elif action == 4:
            if (self.y_coord < self.map_length + self.distance_move) and (self.x_coord < self.map_length + self.distance_move):

                # storing each coordinate of the path going for this one step
                # it will be used to check if IED attack applies
                if not self.drone_mode:
                    self.path_step_x = []
                    self.path_step_y = []
                    for m in range(1, self.distance_move + 1):
                        #self.path_step_x.append(self.list_scenar[x + m])
                        self.path_step_x.append(self.x_coord + m)
                        self.path_step_y.append(self.y_coord + m)

                self.list_scenar[self.y_coord + self.distance_move][self.x_coord + self.distance_move] = self.list_scenar[self.y_coord][self.x_coord]
                self.list_scenar[self.y_coord][self.x_coord] = 0

        # move SOUTH
        elif action == 5:
            if self.y_coord < self.map_length + self.distance_move:

                # storing each coordinate of the path going for this one step
                # it will be used to check if IED attack applies
                if not self.drone_mode:
                    self.path_step_x = []
                    self.path_step_y = []
                    for m in range(1, self.distance_move + 1):
                        #self.path_step_x.append(self.list_scenar[x + m])
                        self.path_step_x.append(self.x_coord)
                        self.path_step_y.append(self.y_coord + m)

                self.list_scenar[self.y_coord + self.distance_move][self.x_coord] = self.list_scenar[self.y_coord][self.x_coord]
                self.list_scenar[self.y_coord][self.x_coord] = 0

        # move SOUTH-WEST
        elif action == 6:
            if (self.y_coord < self.map_length + self.distance_move) and (self.x_coord > self.distance_move):

                # storing each coordinate of the path going for this one step
                # it will be used to check if IED attack applies
                if not self.drone_mode:
                    self.path_step_x = []
                    self.path_step_y = []
                    for m in range(1, self.distance_move + 1):
                        #self.path_step_x.append(self.list_scenar[x + m])
                        self.path_step_x.append(self.x_coord - m)
                        self.path_step_y.append(self.y_coord + m)

                self.list_scenar[self.y_coord + self.distance_move][self.x_coord - self.distance_move] = self.list_scenar[self.y_coord][self.x_coord]
                self.list_scenar[self.y_coord][self.x_coord] = 0

        # move WEST
        elif action == 7:
            if self.x_coord > self.distance_move:

                # storing each coordinate of the path going for this one step
                # it will be used to check if IED attack applies
                if not self.drone_mode:
                    self.path_step_x = []
                    self.path_step_y = []
                    for m in range(1, self.distance_move + 1):
                        #self.path_step_x.append(self.list_scenar[x + m])
                        self.path_step_x.append(self.x_coord - m)
                        self.path_step_y.append(self.y_coord)

                self.list_scenar[self.y_coord][self.x_coord - 1] = self.list_scenar[self.y_coord][self.x_coord]
                self.list_scenar[self.y_coord][self.x_coord] = 0

        # move NORTH-WEST
        elif action == 8:
            if (self.y_coord > self.distance_move) and (self.x_coord > self.distance_move):

                # storing each coordinate of the path going for this one step
                # it will be used to check if IED attack applies
                if not self.drone_mode:
                    self.path_step_x = []
                    self.path_step_y = []
                    for m in range(1, self.distance_move + 1):
                        #self.path_step_x.append(self.list_scenar[x + m])
                        self.path_step_x.append(self.x_coord - m)
                        self.path_step_y.append(self.y_coord - m)

                self.list_scenar[self.y_coord - self.distance_move][self.x_coord - self.distance_move] = self.list_scenar[self.y_coord][self.x_coord]
                self.list_scenar[self.y_coord][self.x_coord] = 0

        # do nothing
        elif action == 9:
            pass

        # check if new coordinate is an IED
        if self.x_coord == self.x_coord_ied and self.y_coord == self.y_coord_ied:
            print("IED!")
            self.ied_attack = True
        # check if entity passed IED when drone mode is off
        if not self.drone_mode and action != 9: #and len(self.path_step_x) == self.distance_move:
            for m in range(len(self.path_step_x)):
                if self.x_coord_ied == self.path_step_x[m] and self.y_coord_ied == self.path_step_y[m]:
                    self.ied_attack = True
                    print("Passed IED!")
                    time.sleep(5)


        # calculate the distance to the goal
        self.distance_goal = math.sqrt((self.x_coord - self.x_coord_goal) ** 2 + (self.y_coord - self.y_coord_goal) ** 2)

        # setting the reward here
        if self.distance_goal > 1:
            reward = -1
        else:
            reward = 0

        # check if Goal (Flag) is captured, episode is ended or IED is hit
        if (self.episode_length <= 0) or (self.distance_goal < 2) or (self.ied_attack == True):
            done = True

            if self.ied_attack:
                reward = -self.episode_length - 1
                #reward = 100
                print("Reward: ", reward)
                print("Episode Length: ", self.episode_length)

            # write path tracking lists to csv file with timestamp, when path tracking is True
            # check if episode is done or episode length has ended
            if self.path_tracking:
                # combine list for x and y coordinate
                self.path_x_y = []
                for i in range(len(self.path_track_x)):
                    self.coord_path = []
                    self.coord_path.append(self.path_track_x[i])
                    self.coord_path.append(self.path_track_y[i])
                    self.path_x_y.append(self.coord_path)
                timestamp = time.time()

                # create path filename with timestamp
                path_filename = "path_tracking/Path_" + str(timestamp) + ".csv"

                # create file and write to file
                with open(path_filename, 'w') as f:
                    write = csv.writer(f)
                    fields = ['x', 'y']
                    write.writerow(fields)
                    write.writerows(self.path_x_y)

        else:
            done = False



        # get observation_space
        self.observation_space = merge_obspace.get_obspace(self.observation_space, self.list_map, self.list_scenar, self.map_length)

        # reduce episode length by 1 one at the end of the step
        self.episode_length -= 1


        info = {}

        return self.observation_space, reward, done, info



    def render(self):
        # clear screen for rendering new frame of the map
        os.system('clear')

        # get observation_space
        self.observation_space = merge_obspace.get_obspace(self.observation_space, self.list_map, self.list_scenar, self.map_length)

        # render map in terminal
        for y in range(self.map_length):
            for x in range(self.map_length):
                if self.observation_space[y][x] == 90:
                    print(Back.GREEN + '  ', end=" " + Back.BLACK)
                elif self.observation_space[y][x] == 92:
                    print(Back.WHITE + '  ', end=" " + Back.BLACK)
                elif self.observation_space[y][x] == 91:
                    print(Back.YELLOW + '  ', end=" " + Back.BLACK)
                elif self.observation_space[y][x] == 93:
                    print(Back.BLUE + '  ', end=" " + Back.BLACK)
                elif self.observation_space[y][x] == 99:
                    print(Back.MAGENTA + ' G', end=" " + Back.BLACK)
                elif self.observation_space[y][x] == 10:
                    print(Back.CYAN + ' T', end=" " + Back.BLACK)
                elif self.observation_space[y][x] == 80:
                    print(Back.RED + ' B', end=" " + Back.BLACK)
            print("")

        print(f"Distance to goal: {round(self.distance_goal, 2)}\n")



    def reset(self):
        if self.path_tracking:
            self.path_track_x = []
            self.path_track_y = []

        self.episode_length = self.timesteps

        self.ied_attack = False

        done = False

        # Reset Scenar List
        with open(self.scenar_file, newline='') as csvfile_scenar:
            self.list_scenar = list(csv.reader(csvfile_scenar, delimiter=';'))
        # convert scenar list to int
        for y in range(self.map_length):
            for x in range(self.map_length):
                self.list_scenar[y][x] = int(self.list_scenar[y][x])

        # get observation_space
        self.observation_space = merge_obspace.get_obspace(self.observation_space, self.list_map, self.list_scenar, self.map_length)

        return self.observation_space