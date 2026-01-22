from __builtins__ import *
import boundaries
import movement
import lib_maze


## Runs a dinosaur farming loop by directly heading to the next apple.
## This will fail pretty fast but does not waste time with unnecessary movements.
def farming_dinosaur_simple():
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



## Runs a dinosaur farming loop.
## This variant tries to avoid collision by moving in a zigzag pattern
## and so fill the entire world.
def farming_dinosaur():
    # path covering all but the left column, which we need to return to the origin
    bounds = boundaries.make_world_bounds()
    bounds[0] = 1

    max_coordinate = get_world_size() - 1

    current_tail_length = 0
    is_in_bounds = True

    skippable_rows = max_coordinate
    skips_in_use = []

    boundaries.move_to_origin(bounds)

    # start the game
    change_hat(Hats.Dinosaur_Hat)
    apple_pos = measure()

    def add_skip(n=1):
        for _i in range(n):
            skips_in_use.append(current_tail_length + 1)

    while True:
        current_pos = (get_pos_x(), get_pos_y())
        next_dir = None

        # decay all currently used skips
        for i in range(len(skips_in_use)-1, -1, -1):
            skips_in_use[i] = skips_in_use[i] - 1
            if skips_in_use[i] <= 0:
                skips_in_use.pop(i)

        if current_pos == apple_pos:
            current_tail_length = current_tail_length + 1

            # recompute the maximum number of rows we can skip
            skippable_rows = max_coordinate - (current_tail_length // max_coordinate) - 1

            apple_pos = measure()

        if is_in_bounds:
            if skippable_rows > len(skips_in_use):
                if current_pos[0] == apple_pos[0] and current_pos[1] < apple_pos[1] and current_pos[1] != max_coordinate:
                    # apple is on the same column
                    next_dir = North
                    add_skip()
                elif current_pos[1] > apple_pos[1]:
                    skips_needed = max_coordinate - current_pos[1]

                    # apple is below the drone, then just move out of the bounds
                    if current_pos[1] % 2 == 0:
                        # exception on even rows, this may lead into a collision
                        next_dir = North
                        add_skip()
                    # check if we can skip all rows above
                    elif skippable_rows > (len(skips_in_use) + skips_needed):
                        if current_pos[0] == 1:
                            is_in_bounds = False
                            add_skip(skips_needed)
                        next_dir = West
                elif current_pos[1] < apple_pos[1] and apple_pos[0] == 0:
                    # apple is in the leftmost column (not in bounds) and above the drone
                    next_dir = North
                    add_skip()

            if next_dir == None:
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

        while not can_move(next_dir):
            do_a_flip()

        did_move = move(next_dir)

        # when not able to move anymore, harvest the bones and return
        if not did_move:
            change_hat(Hats.Brown_Hat)
            return
