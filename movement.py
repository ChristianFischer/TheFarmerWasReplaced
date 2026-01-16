from __builtins__ import *
import boundaries


Movement_Step = 0
Movement_Next_Row = 1
Movement_Done = 2


def fly_over_field(per_field_callback):
    while True:
        per_field_callback()

        if fly_field_step():
            return


def fly_field_step():
    move(East)
    if get_pos_x() == 0:
        move(North)

        if get_pos_y() == 0:
            return True

    return False


def fly_field_step_in_bounds(bounds):
    min_x, min_y, max_x, max_y = bounds
    x = get_pos_x()
    y = get_pos_y()

    # if outside the boundaries, move to origin first
    if x < min_x or x > max_x or y < min_y or y > max_y:
        ox, oy = boundaries.get_origin(bounds)
        move_to(ox, oy)
        return False

    mod = (y - min_y) % 2
    if mod == 0:
        if x == max_x:
            if y == max_y:
                return True
            else:
                move(North)
        else:
            move(East)
    else:
        if x == min_x:
            if y == max_y:
                return True
            else:
                move(North)
        else:
            move(West)

    return False


def fly_field_step_in_bounds_with_state(bounds):
    min_x, min_y, max_x, max_y = bounds
    x = get_pos_x()
    y = get_pos_y()

    # if outside the boundaries, move to origin first
    if x < min_x or x > max_x or y < min_y or y > max_y:
        ox, oy = boundaries.get_origin(bounds)
        move_to(ox, oy)
        return Movement_Step

    mod = (y - min_y) % 2
    if mod == 0:
        if x == max_x:
            if y == max_y:
                return Movement_Done
            else:
                move(North)
                return Movement_Next_Row
        else:
            move(East)
    else:
        if x == min_x:
            if y == max_y:
                return Movement_Done
            else:
                move(North)
                return Movement_Next_Row
        else:
            move(West)

    return Movement_Step


def fly_field_step_in_bounds_reverse(bounds):
    min_x, min_y, max_x, max_y = bounds
    x = get_pos_x()
    y = get_pos_y()

    # if outside the boundaries, move to the path end first
    if x < min_x or x > max_x or y < min_y or y > max_y:
        ex, ey = boundaries.get_path_end(bounds)
        move_to(ex, ey)
        return False

    mod = (y - min_y) % 2
    if mod == 0:
        if x == min_x:
            if y == min_y:
                return True
            else:
                move(South)
        else:
            move(West)
    else:
        if x == max_x:
            if y == min_y:
                return True
            else:
                move(South)
        else:
            move(East)

    return False


def fly_field_step_in_bounds_get_next_dir(bounds):
    min_x, min_y, max_x, max_y = bounds
    x = get_pos_x()
    y = get_pos_y()

    # invalid, if outside boundaries
    if x < min_x or x > max_x or y < min_y or y > max_y:
        return None

    mod = (y - min_y) % 2
    if mod == 0:
        if x == max_x:
            if y == max_y:
                return None # finished
            else:
                return North
        else:
            return East
    else:
        if x == min_x:
            if y == max_y:
                return None # finished
            else:
                return North
        else:
            return West


def move_to(x, y):
    ws = get_world_size()

    pos_x = get_pos_x()
    dist_w = pos_x + ws - x
    dist_e = x - pos_x
    if dist_w < dist_e:
        dir_x = West
        off_x = -1
    else:
        dir_x = East
        off_x = +1
    while pos_x != x:
        move(dir_x)
        pos_x = (pos_x + off_x) % ws

    pos_y = get_pos_y()
    dist_s = pos_y + ws - y
    dist_n = y - pos_y
    if dist_s < dist_n:
        dir_y = South
        off_y = -1
    else:
        dir_y = North
        off_y = +1
    while pos_y != y:
        move(dir_y)
        pos_y = (pos_y + off_y) % ws


def move_to_no_wrap(x, y):
    while get_pos_x() < x:
        move(East)
    while get_pos_x() > x:
        move(West)
    while get_pos_y() < y:
        move(North)
    while get_pos_y() > y:
        move(South)


def reset_world_pos():
    while get_pos_x() > 0:
        move(West)

    while get_pos_y() > 0:
        move(South)


def is_on_start():
    if get_pos_x() == 0 and get_pos_y() == 0:
        return True
    return False
