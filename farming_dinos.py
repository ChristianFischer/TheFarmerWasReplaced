from __builtins__ import *
import boundaries
import movement
import lib_maze


def farming_dinosaur():
    clear()
    change_hat(Hats.Dinosaur_Hat)
    apple_pos = measure()

    while True:
        current_pos = (get_pos_x(), get_pos_y())
        apple_dir = lib_maze.get_relative_dir(current_pos, apple_pos)

        if apple_dir == None:
            apple_pos = measure()
            continue

        did_move = move(apple_dir)
        if not did_move:
            did_move = move(lib_maze.turn_left(apple_dir))
        if not did_move:
            did_move = move(lib_maze.turn_right(apple_dir))
        if not did_move:
            did_move = move(lib_maze.turn_back(apple_dir))

        # when not able to move anymore, harvest the bones and return
        if not did_move:
            change_hat(Hats.Brown_Hat)
            return



# not meant for production, only achievement
def farming_dinosaur_stupid_path():
    # path covering all but the left column, which we need to return to the origin
    bounds = boundaries.make_world_bounds()
    bounds[0] = 1
    is_in_bounds = True

    boundaries.move_to_origin(bounds)

    # start the game
    change_hat(Hats.Dinosaur_Hat)

    while True:
        if is_in_bounds:
            next_dir = movement.fly_field_step_in_bounds_get_next_dir(bounds)
            if next_dir == None:
                is_in_bounds = False
                next_dir = West
        else:
            if get_pos_y() > 0:
                next_dir = South
            else:
                next_dir = East
                is_in_bounds = True

        did_move = move(next_dir)

        # when not able to move anymore, harvest the bones and return
        if not did_move:
            change_hat(Hats.Brown_Hat)
            return
