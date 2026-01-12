from __builtins__ import *
from lib_maze import *


def run_maze(times=1):
    harvest()
    plant(Entities.Bush)

    required_substance = calc_required_substance()
    use_item(Items.Weird_Substance, required_substance)

    do_a_flip()

    current_dir = North

    while True:
        current_x = get_pos_x()
        current_y = get_pos_y()

        d = turn_right(current_dir)
        _did_move = move(d)

        while not _did_move:
            d = turn_left(d)
            _did_move = move(d)

        current_dir = d

        if get_entity_type() == Entities.Treasure:
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
