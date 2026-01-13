from __builtins__ import *
import lib_maze


def farming_dinosaur():
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


