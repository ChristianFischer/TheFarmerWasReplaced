from __builtins__ import *
from lib_maze import *


def run_maze(times=1):
    harvest()
    plant(Entities.Bush)

    required_substance = calc_required_substance()
    use_item(Items.Weird_Substance, required_substance)

    do_a_flip()

    use_dfs = False

    while True:
        if use_dfs:
            solve_maze_dfs()
        else:
            solved = solve_maze()

            # if the easy algorithm couldn't solve the maze, use dfs from now on
            if not solved:
                use_dfs = True
                continue

        if get_entity_type() == Entities.Treasure:
            # to repeat, use again the weird substance on the chest
            if times > 1:
                if num_items(Items.Weird_Substance) < required_substance:
                    print("Not enough weird substances!")
                    harvest()
                    return

                use_item(Items.Weird_Substance, required_substance)
                times = times - 1
            else:
                harvest()
                return
        else:
            print("Failed to solve the maze")
            return



def solve_maze():
    max_num_steps = get_world_size() * get_world_size() * 2
    current_dir = North

    while True:
        d = turn_right(current_dir)

        _did_move = move(d)

        while not _did_move:
            d = turn_left(d)
            _did_move = move(d)

        current_dir = d

        if get_entity_type() == Entities.Treasure:
            return True

        # if we did too much steps, we're probably inside a loop
        max_num_steps -= 1
        if max_num_steps <= 0:
            return False



def solve_maze_dfs():
    treasure_pos = measure()
    visited = []

    for _i in range(get_world_size() ** 2):
        visited.append(False)

    return dfs_step(visited, treasure_pos)


def dfs_step(visited, treasure_pos, direction=None):
    current_pos = (get_pos_x(), get_pos_y())
    current_pos_index = get_pos_index(current_pos[0], current_pos[1])
    visited[current_pos_index] = True

    if get_entity_type() == Entities.Treasure:
        # solved!
        return True

    # prefer the treasure direction
    treasure_dir = get_relative_dir(current_pos, treasure_pos)

    if direction == None:
        possible_dirs = [treasure_dir, North, West, South, East]
    else:
        possible_dirs = [treasure_dir, direction, turn_left(direction), turn_right(direction)]

    for d in possible_dirs:
        if can_move(d):
            neighbour_index = get_pos_index_in_dir(d)
            if not visited[neighbour_index]:
                move(d)

                solved = dfs_step(visited, treasure_pos, d)
                if solved:
                    return True

                move(turn_back(d))

    return False
