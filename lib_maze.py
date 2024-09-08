from __builtins__ import *


def turn_left(_d):
    _directions_left = { West: South, South: East, East: North, North: West}
    return _directions_left[_d]
    # if _d == West:
    #     return South
    # if _d == South:
    #     return East
    # if _d == East:
    #     return North
    # if _d == North:
    #     return West


def turn_right(_d):
    _directions_right = { West: North, North: East, East: South, South: West}
    return _directions_right[_d]
    # if _d == West:
    #     return North
    # if _d == North:
    #     return East
    # if _d == East:
    #     return South
    # if _d == South:
    #     return West
