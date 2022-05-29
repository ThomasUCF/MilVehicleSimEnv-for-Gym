# GymTankSimEnv
**MAP CSV-File:**<br>
    90  Forrest<br>
    91  Sand<br>
    92  Road<br>
    93  Water<br>
    Map is loaded as list and can be accessed with list_map[y][x]
    
**Scenar CSV-File:**<br>
    10  Tank<br>
    99  Goal (Flag)<br>
    Scenar is loaded as list and can be accessed with list_map[y][x]
    
**Action Space:**<br>
    1   Move up<br>
    2   Move Right<br>
    3   Move Down<br>
    4   Move Left<br>
    5   Do Nothing
    
**Observatgion Space:**<br>
    Combination of Map List and Scenar List; uses module merge_obspace<br>
    Size: 64 x 64

**Drone Mode:**<br>
    When set to True Drone Mode is activated. This means, that speed is always the same no matter what terrain.

**Path Tracking**<br>
    If Path tracking is true, each episode will write the path of the tank/drone to a csv-file<br>
    The csv-file as the format:<br>
    First Row: x,y<br>
    Following Rows: x-coordinate-step, y-coordinate-step<br>
