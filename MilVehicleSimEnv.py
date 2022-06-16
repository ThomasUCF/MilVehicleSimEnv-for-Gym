'''
Author: Thomas Schiller, M&S Student
University: University of Central Florida
Institute: Institute for Simulation and Training
'''

import csv
import math
import os
import time
from gym import Env
from gym.spaces import Discrete, Box
from colorama import Fore, Back, Style
import merge_obspace
import reduce_obspace

class MilVehicleSimEnv(Env):
    def __init__(self):
        '''
        The following setting can be set by the user to change the characteristics of the simulation
        '''

        # set Map and Scenar File!
        self.map_file = "maps/Map01_TankSimEnv.csv"
        self.scenar_file = "scenars/Scenar03_TankSimEnv.csv"

        # set Path Tracking
        self.path_tracking = True

        # User settings: set Drone Mode
        self.drone_mode = False
        # User settings: set Drone Speed
        self.speed_drone = 1  # should not be more than 3

        # User setting: IED Mode
        self.ied_mode = True
        # User setting: show IEDs to user in rendering
        self.show_ied = True

        # User setting: Set episode length
        self.timesteps = 120

        # User setting: set if observation space is reduced
        self.reduced_obspace = True


        '''
        The following settings and initialization are no user setting
        '''

        # initialize the timesteps
        self.episode_length = self.timesteps

        # initialize the path tracking
        if self.path_tracking:
            self.path_track_x = []
            self.path_track_y = []

        # set map size (needs to correlate with csv-file size!)
        self.map_length = 64

        # set terrain constraints
        self.speed_road = 3
        self.speed_sand = 2
        self.speed_forrest = 1

        # set Boolean for IED activation
        self.ied_attack = False

        #set Boolean for Goal Reached
        self.goal_reached = False

        # load map file
        with open(self.map_file, newline='') as csvfile_map:
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
        if self.ied_mode:
            for y in range(self.map_length):
                for x in range(self.map_length):
                    if self.list_scenar[y][x] == 80:
                        self.y_coord_ied = y
                        self.x_coord_ied = x
                        pass

        # Set the Action Space
        self.action_space = Discrete(9)

        # Set the Framework List for the Observation Space
        with open(self.map_file, newline='') as csvfile_observation_space:
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
                # this is the actual move; it writes the new coordinate in the scenar list
                self.list_scenar[self.y_coord - self.distance_move][self.x_coord] = self.list_scenar[self.y_coord][self.x_coord]
                self.list_scenar[self.y_coord][self.x_coord] = 0



        # move NORTH-EAST
        elif action == 2:
            if (self.x_coord < self.map_length + self.distance_move) and (self.y_coord > self.distance_move):
                # this is the actual move; it writes the new coordinate in the scenar list
                self.list_scenar[self.y_coord - self.distance_move][self.x_coord + self.distance_move] = self.list_scenar[self.y_coord][self.x_coord]
                self.list_scenar[self.y_coord][self.x_coord] = 0

        # move EAST
        elif action == 3:
            if self.x_coord < self.map_length - self.distance_move:
                # this is the actual move; it writes the new coordinate in the scenar list
                self.list_scenar[self.y_coord][self.x_coord + self.distance_move] = self.list_scenar[self.y_coord][self.x_coord]
                self.list_scenar[self.y_coord][self.x_coord] = 0

        # move SOUTH-EAST
        elif action == 4:
            if (self.y_coord < self.map_length + self.distance_move) and (self.x_coord < self.map_length + self.distance_move):
                # this is the actual move; it writes the new coordinate in the scenar list
                self.list_scenar[self.y_coord + self.distance_move][self.x_coord + self.distance_move] = self.list_scenar[self.y_coord][self.x_coord]
                self.list_scenar[self.y_coord][self.x_coord] = 0

        # move SOUTH
        elif action == 5:
            if self.y_coord < self.map_length - self.distance_move:
                # this is the actual move; it writes the new coordinate in the scenar list
                self.list_scenar[self.y_coord + self.distance_move][self.x_coord] = self.list_scenar[self.y_coord][self.x_coord]
                self.list_scenar[self.y_coord][self.x_coord] = 0

        # move SOUTH-WEST
        elif action == 6:
            if (self.y_coord < self.map_length + self.distance_move) and (self.x_coord > self.distance_move):
                # this is the actual move; it writes the new coordinate in the scenar list
                self.list_scenar[self.y_coord + self.distance_move][self.x_coord - self.distance_move] = self.list_scenar[self.y_coord][self.x_coord]
                self.list_scenar[self.y_coord][self.x_coord] = 0

        # move WEST
        elif action == 7:
            if self.x_coord > self.distance_move:
                # this is the actual move; it writes the new coordinate in the scenar list
                self.list_scenar[self.y_coord][self.x_coord - 1] = self.list_scenar[self.y_coord][self.x_coord]
                self.list_scenar[self.y_coord][self.x_coord] = 0

        # move NORTH-WEST
        elif action == 8:
            if (self.y_coord > self.distance_move) and (self.x_coord > self.distance_move):
                # this is the actual move; it writes the new coordinate in the scenar list
                self.list_scenar[self.y_coord - self.distance_move][self.x_coord - self.distance_move] = self.list_scenar[self.y_coord][self.x_coord]
                self.list_scenar[self.y_coord][self.x_coord] = 0

        # do nothing
        elif action == 9:
            pass

        # calculate the distance to the goal
        self.distance_goal = math.sqrt((self.x_coord - self.x_coord_goal) ** 2 + (self.y_coord - self.y_coord_goal) ** 2)
        # check if goal is reached
        if self.distance_goal <= 2:
            self.goal_reached = True

        # calculate the direction to the goal
        self.angle_to_goal = math.atan2(self.y_coord - self.y_coord_goal, self.x_coord - self.x_coord_goal)
        self.angle_to_goal = round(math.degrees(self.angle_to_goal), 0)
        #print(self.angle_to_goal)

        # describe the angle in N E S or W
        if self.angle_to_goal >= -135 and self.angle_to_goal <= -45:
            self.goal_direction = 1
        elif self.angle_to_goal > -45 and self.angle_to_goal < 45:
            self.goal_direction = 2
        elif self.angle_to_goal >= 45 and self.angle_to_goal <= 135:
            self.goal_direction = 3
        elif self.angle_to_goal > 135 and self.angle_to_goal <= 180 or self.angle_to_goal < -135 and self.angle_to_goal >=-180:
            self.goal_direction = 4
        else:
            self.goal_direction = 0

        # setting the reward here
        if self.distance_goal > 1:
            reward = -1
        else:
            reward = 0

        # calculate the distance to IED
        if self.ied_mode:
            self.distance_ied = math.sqrt((self.x_coord - self.x_coord_ied) ** 2 + (self.y_coord - self.y_coord_ied) ** 2)
            # check if distance to IED is requirement of IED activation
            if self.distance_ied <= 2:
                self.ied_attack = True

        # check if Goal (Flag) is captured, episode is ended or IED is hit
        if (self.episode_length <= 0) or (self.distance_goal < 2) or (self.ied_attack == True):
            done = True

            if self.ied_attack:
                reward = -self.episode_length - 1
                #print("IED!")  # for debugging purpose
                #print("Reward: ", reward)  # for debugging purpose
                #print("Episode Length: ", self.episode_length)  # for debugging purpose

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

        # reduce observation space if needed
        if self.reduced_obspace:
            self.reduced_obspace_list = reduce_obspace.reduce_obspace(self.observation_space, self.map_length)
            #print(self.reduced_obspace_list)

            # append the distance and the direction to the goal to the observation space
            self.obspace_line_dist_goal = []
            for i in range(len(self.reduced_obspace_list[0])):
                if i == 0:
                    self.obspace_line_dist_goal.append(int(round(self.distance_goal / 10, 0)))
                elif i == 1:
                    self.obspace_line_dist_goal.append(int(self.goal_direction))
                    #self.obspace_line_dist_goal.append(int(self.angle_to_goal))
                else:
                    self.obspace_line_dist_goal.append(0)
            self.reduced_obspace_list.append(self.obspace_line_dist_goal)

            #print(self.reduced_obspace_list)


        # reduce episode length by 1 one at the end of the step
        self.episode_length -= 1


        info = {}

        if self.reduced_obspace:
            return self.reduced_obspace_list, reward, done, info

        if not self.reduced_obspace:
            return self.observation_space, reward, done, info



    def render(self):
        # clear screen for rendering new frame of the map
        os.system('clear')

        # get observation_space
        self.observation_space_render = merge_obspace.get_obspace_render(self.observation_space, self.list_map, self.list_scenar, self.map_length, self.ied_mode, self.show_ied)

        # render map in terminal
        for y in range(self.map_length):
            for x in range(self.map_length):
                if self.observation_space_render[y][x] == 90:
                    print(Back.GREEN + '  ', end=" " + Back.BLACK)
                elif self.observation_space_render[y][x] == 92:
                    print(Back.WHITE + '  ', end=" " + Back.BLACK)
                elif self.observation_space_render[y][x] == 91:
                    print(Back.YELLOW + '  ', end=" " + Back.BLACK)
                elif self.observation_space_render[y][x] == 93:
                    print(Back.BLUE + '  ', end=" " + Back.BLACK)
                elif self.observation_space_render[y][x] == 99:
                    print(Back.MAGENTA + ' G', end=" " + Back.BLACK)
                elif self.observation_space_render[y][x] == 10:
                    print(Back.CYAN + ' T', end=" " + Back.BLACK)
                elif self.ied_mode:
                    if self.show_ied:
                        if self.observation_space_render[y][x] == 80:
                            print(Back.RED + ' B', end=" " + Back.BLACK)
            print("")

        if self.episode_length <= 59:
            print(f"Distance to goal: {round(self.distance_goal, 2)}\n")



    def reset(self):
        if self.path_tracking:
            self.path_track_x = []
            self.path_track_y = []

        self.episode_length = self.timesteps

        # reset IED activation
        self.ied_attack = False

        # reset goal reached
        self.goal_reached = False

        # reset episode DONE
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

        if self.reduced_obspace:
            self.reduced_obspace_list = reduce_obspace.reduce_obspace(self.observation_space, self.map_length)

        if self.reduced_obspace:
            return self.reduced_obspace_list
        if not self.reduced_obspace:
            return self.observation_space