import numpy as np
from matplotlib import pyplot as plt
import click
import time

def show_map(filename, save_map):
    # set image file
    #image_file = 'maps/Map01_TankSimEnv.csv'
    image_file = filename

    # set the color codes
    colorcode_forrest = np.array([191, 242, 128])
    colorcode_sand = np.array([253, 251, 239])
    colorcode_road = np.array([160, 160, 160])

    # load image from csv file
    image_data = np.genfromtxt(image_file, delimiter=';')

    rgb_image = np.zeros([64,64,3], dtype=int)

    for y in range(64):
        #print(rgb_line)
        for x in range(64):
            if image_data[x,y] == 90:
                rgb_image[x,y] = colorcode_forrest
            if image_data[x,y] == 91:
                rgb_image[x,y] = colorcode_sand
            if image_data[x,y] == 92:
                rgb_image[x,y] = colorcode_road

    # for debugging
    #print(np.shape(rgb_image))
    #print(rgb_image)

    plt.clf()
    plt.imshow(rgb_image, interpolation='nearest')
    plt.title("Analysis of Formation")

    if save_map == 1:
        tc = time.time()
        image_filename = str(tc) + ".png"
        print (image_filename)
        plt.savefig(image_filename)
    else:
        plt.show()


@click.command()
@click.argument('option')
@click.option('--filename', default ='maps/Map01_TankSimEnv.csv',
        help ='Set map that should be loaded.')

def main(option, filename):
    '''
    This tool is to show a graphical map from a csv file.


    The following commands are available:


    MapViewer showmap --filename  --> Show Map in Windows

    MapViewer savemap --filename  --> Saves Map as PNG-File

    '''
    if option == "showmap":
        show_map(filename, 0)
    if option == "savemap":
        show_map(filename, 1)

if __name__ == "__main__":
    main()