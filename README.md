# GymTankSimEnv
**Latest edit:** 06/01/2022<br>
**Author:** Thomas Schiller<br>
**University:** University of Central Florida (UCF)<br>
**Institute:** Institute for Simulation and Training<br>

## Introduction
This is a custom gym environment simulating a tank or drone movement on a custom map of 64x64 size.<br>
The simulation is a single agent based. At the moment it can only handle one entity.

![](img/gymtankenv_screenshot.png)

## Map Files and Handling

Maps can be created with an Excel tool and are stored in a csv file. The tool and csv map files are stored in the "maps" folder.<br>
Each grid on the map is defined by the following code:

|Code   |Element    |
|-------|-----------|
|90     |Forrest    |
|91     |Sand       |
|92     |Road       |
|93     |Water      |

Map is loaded as list and can be accessed with `list_map[y][x]`

### ShowMap Tool
This tool is to show a graphical map from a map csv file. It has a command line interface (CLI) and can be used in terminal or command line.<br>

Use the help command for how to use this tool:

	MapViewer --help
	
   The following commands are available:
    
	MapViewer showmap --filename  --> Show Map in Windows
	MapViewer savemap --filename  --> Saves Map as PNG-File

Standard --filename is "maps/Map01_TankSimEnv.csv".
    
## Scenar Files and Handling

Scenars can be created with an Excel tool and are stored in a csv file. The tool and csv scenar files are stored in the "scenars" folder.<br>
Each grid of the scenar is defined by the following code:

|Code   |Element    |
|-------|-----------|
|10     |Tank/Drone |
|99     |Goal/Flag  |

Scenar is loaded as list and can be accessed with `list_map[y][x]`
    
## Action Space

|Action|Movement   |
|------|-----------|
|1     |Move Up    |
|2     |Move Right |
|3     |Move Down  |
|4     |Move Left  |
|4     |Do Nothing |
    
## Observatgion Space
Combination of Map List and Scenar List; uses module merge_obspace<br>
Size: 64 x 64

## Reward
Worst Possible Reward: -61
Best Theoretical Reward: 0

Reward is similar to Mountain Car. The higher the value, the better the result.

## Drone Mode:
A drone mode can be activated. This means, that the speed is always the same no matter what terrain.

	# set Drone Mode
	self.drone_mode = True
	self.speed_drone = 1

## Path Tracking
If Path tracking is true, each episode will write the path of the tank/drone to a csv-file<br>

    # set Path Tracking
    self.path_tracking = True

The csv-file as the format:

|x                    |y                    |
|---------------------|---------------------|
|x-coordinate 1. step |y-coordinate 1. step |
|x-coordinate 2. step |y-coordinate 2. step |
|x-coordinate n. step |y-coordinate n. step |
    
    
### Path Tracking Tool: Single Path
This tool displays a tracked path with the map and scenar.<br>
Map, scenar and path must be set at the beginning of the file:

	map_file = 'maps/Map01_TankSimEnv.csv'
	scenar_file = 'scenars/Scenar01_TankSimEnv.csv'
	path_file = 'path_tracking/Path_1654107091.868553.csv'
	
The tool will print the path from the path file:
![](img/single_path_track_plot.png)

### Path Tracking Tool: Multi Path
tbd