def fly_over_field():
    move(East)
    if get_pos_x() == 0:
        move(South)

        if get_pos_y() == get_world_size()-1:
            return True

    return False


def reset_world_pos():
    while get_pos_x() > 0:
        move(West)

    while get_pos_y() > 0:
        move(South)


def is_on_start():
    if get_pos_x() == 0 and get_pos_y() == 0:
        return True
    return False