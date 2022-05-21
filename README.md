# GymTankSimEnv
**MAP CSV-File:**
    90  Forrest
    91  Sand
    92  Road
    93  Water
    Map is loaded as list and can be accessed with list_map[y][x]
**Scenar CSV-File:**
    10  Tank
    99  Goal (Flag)
    Scenar is loaded as list and can be accessed with list_map[y][x]
**Action Space:**
    1   Move up
    2   Move Right
    3   Move Down
    4   Move Left
    5   Do Nothing
**Observatgion Space:**
    Combination of Map List and Scenar List; uses module merge_obspace
    Size: 64 x 64
