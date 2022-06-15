'''
Author: Thomas Schiller, M&S Student
University: University of Central Florida
Institute: Institute for Simulation and Training
'''


def get_obspace_render(observation_space, list_map, list_scenar, map_length, ied_mode, show_ied):
    for y in range(map_length):
        for x in range(map_length):
            observation_space[y][x] = list_map[y][x]
    for y in range(map_length):
        for x in range(map_length):
            if list_scenar[y][x] > 0:
                observation_space[y][x] = list_scenar[y][x]
                if ied_mode:
                    if not show_ied:
                        if observation_space[y][x] == 80:
                            observation_space[y][x] = list_map[y][x]
                if not ied_mode:
                    if observation_space[y][x] == 80:
                        observation_space[y][x] = list_map[y][x]

    return observation_space

'''
# merge observation space with goal viewable
def get_obspace(observation_space, list_map, list_scenar, map_length):
    for y in range(map_length):
        for x in range(map_length):
            observation_space[y][x] = list_map[y][x]
    for y in range(map_length):
        for x in range(map_length):
            if list_scenar[y][x] > 0:
                observation_space[y][x] = list_scenar[y][x]
            if list_scenar[y][x] == 80:
                observation_space[y][x] = list_map[y][x]
'''

# merge observation space without goal viewable
# reduces Q-Table!
def get_obspace(observation_space, list_map, list_scenar, map_length):
    for y in range(map_length):
        for x in range(map_length):
            observation_space[y][x] = list_map[y][x]
    for y in range(map_length):
        for x in range(map_length):
            if list_scenar[y][x] == 10:
                observation_space[y][x] = list_scenar[y][x]

    return observation_space