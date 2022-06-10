'''
Author: Thomas Schiller
University: University of Central Florida
Institute: Institute for Simulation and Training
'''

map_length = 64

#reduced_obspace_size = 25  # 5 x 5
reduced_obspace_size = 49  # 7 x 7

def reduce_obspace(obspace, map_length):
    #entity_x_coord = 0
    #entity_y_coord = 0

    # getting the x- and y- coordinate of the entity
    for y in range(map_length):
        for x in range(map_length):
            if obspace[y][x] == 10:
                entity_x_coord = x
                entity_y_coord = y
                #print("Coordinate Entity: ", entity_x_coord, ",", entity_y_coord)

    if reduced_obspace_size == 25:
        # create an empty reduced observation space
        obspace_red = []
        for m in range(5):
            obspace_red_line = []
            for n in range(5):
                obspace_red_line.append(0)
            obspace_red.append(obspace_red_line)

        #print(obspace_red)  # for debugging

        # check if entity is near border of the map
        for m, y in zip(range(-2, 3), range(5)):
            for n, x in zip(range(-2, 3), range(5)):
                if entity_y_coord + m > - 1 and entity_x_coord + n > - 1 and entity_y_coord + m < map_length and entity_x_coord + n < map_length:
                    obspace_red[y][x] = obspace[entity_y_coord + m][entity_x_coord + n]
                else:
                    obspace_red[y][x] = 11

    if reduced_obspace_size == 49:
        # create an empty reduced observation space
        obspace_red = []
        for m in range(7):
            obspace_red_line = []
            for n in range(7):
                obspace_red_line.append(0)
            obspace_red.append(obspace_red_line)

        # print(obspace_red)  # for debugging

        # check if entity is near border of the map
        for m, y in zip(range(-3, 4), range(7)):
            for n, x in zip(range(-3, 4), range(7)):
                if entity_y_coord + m > - 1 and entity_x_coord + n > - 1 and entity_y_coord + m < map_length and entity_x_coord + n < map_length:
                    obspace_red[y][x] = obspace[entity_y_coord + m][entity_x_coord + n]
                else:
                    obspace_red[y][x] = 11

    return obspace_red
