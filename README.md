# GymTankSimEnv
**MAP CSV-File:**
    90  Forrest<br>
    91  Sand<br>
    92  Road<br>
    93  Water<br>
    Map is loaded as list and can be accessed with list_map[y][x]
    
**Scenar CSV-File:**
    10  Tank<br>
    99  Goal (Flag)<br>
    Scenar is loaded as list and can be accessed with list_map[y][x]
    
**Action Space:**
    1   Move up<br>
    2   Move Right<br>
    3   Move Down<br>
    4   Move Left<br>
    5   Do Nothing
    
**Observatgion Space:**
    Combination of Map List and Scenar List; uses module merge_obspace<br>
    Size: 64 x 64
