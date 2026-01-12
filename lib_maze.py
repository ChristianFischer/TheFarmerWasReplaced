from __builtins__ import *


def calc_required_substance():
    return get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)


def turn_left(_d):
    _directions_left = { West: South, South: East, East: North, North: West}
    return _directions_left[_d]


def turn_right(_d):
    _directions_right = { West: North, North: East, East: South, South: West}
    return _directions_right[_d]
