'''
Author: Thomas Schiller
University: University of Central Florida
Institute: Institute for Simulation and Training
'''


def get_obspace(observation_space, list_map, list_scenar, map_length):
    for y in range(map_length):
        for x in range(map_length):
            observation_space[y][x] = list_map[y][x]
    for y in range(map_length):
        for x in range(map_length):
            if list_scenar[y][x] > 0:
                observation_space[y][x] = list_scenar[y][x]

    return observation_space