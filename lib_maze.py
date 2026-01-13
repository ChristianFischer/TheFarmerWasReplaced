from __builtins__ import *


def calc_required_substance():
    return get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)


def get_pos_index(x, y):
    return x + y * get_world_size()


def get_current_pos_index():
    return get_pos_index(get_pos_x(), get_pos_y())


def get_pos_index_in_dir(d):
    if d == North:
        return get_pos_index(get_pos_x() + 0, get_pos_y() + 1)
    if d == East:
        return get_pos_index(get_pos_x() + 1, get_pos_y() + 0)
    if d == South:
        return get_pos_index(get_pos_x() + 0, get_pos_y() - 1)
    if d == West:
        return get_pos_index(get_pos_x() - 1, get_pos_y() + 0)
    return get_current_pos_index()


def get_relative_dir(origin_pos, target_pos):
    if origin_pos[1] < target_pos[1]:
        return North
    if origin_pos[1] > target_pos[1]:
        return South
    if origin_pos[0] < target_pos[0]:
        return East
    if origin_pos[0] > target_pos[0]:
        return West
    return None


def turn_left(_d):
    _directions_left = { West: South, South: East, East: North, North: West}
    return _directions_left[_d]


def turn_right(_d):
    _directions_right = { West: North, North: East, East: South, South: West}
    return _directions_right[_d]


def turn_back(_d):
    _directions_back = { West: East, South: North, East: West, North: South}
    return _directions_back[_d]
