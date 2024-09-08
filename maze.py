from __builtins__ import *
from farming_sonnenblumen import *
from lib_farming import *
from lib_maze import *

while True:
    do_shopping()
    farming_sonnenblumen_if_necessary()
    t = None

    while t != Entities.Hedge:
        t = get_entity_type()

        if t == Entities.Hedge:
            pass
        elif t == Entities.Bush:
            use_item(Items.Fertilizer)
        elif t == None:
            plant(Entities.Bush)
        else:
            harvest()
            plant(Entities.Bush)

    do_a_flip()

    current_dir = North
    finished = False

    while finished == False:
        current_x = get_pos_x()
        current_y = get_pos_y()

        d = turn_right(current_dir)
        _did_move = move(d)

        while not _did_move:
            d = turn_left(d)
            _did_move = move(d)

        current_dir = d

        if get_entity_type() == Entities.Treasure:
            harvest()

            finished = True
