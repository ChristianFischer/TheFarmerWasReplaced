from __builtins__ import *
from lib_farming import *


def farming_sonnenblumen():
    do_shopping()

    current_max_petals = 0
    petals_list = {}

    # initialize list
    for i in range(16):
        petals_list[i] = 0

    # step1: planting
    for _f in range(get_world_size() * get_world_size()):
        iterate_through_world()

        # plant, if there's not already a sunflower
        if get_entity_type() != Entities.Sunflower:
            if can_harvest():
                harvest()

            do_plant(Entities.Sunflower)

        do_watering()

        # store how much sunflowers we got for each number of petals
        petals = measure()
        petals_list[petals] = petals_list[petals] + 1
        current_max_petals = max(current_max_petals, petals)

    # step2: harvest
    while current_max_petals > 0:
        move(East)
        if get_pos_x() == 0:
            move(South)

        petals = measure()
        if petals == None:
            continue

        # harvest if we're on the current max number of petals
        if petals >= current_max_petals:
            # wait until harvesting is possible
            while can_harvest() == False:
                do_a_flip()

            harvest()

            # decrease number of sunflowers left
            petals_list[petals] = petals_list[petals] - 1

            # continue with next petals size until we're on level 0
            while current_max_petals > 0 and petals_list[current_max_petals] == 0:
                current_max_petals -= 1
                # print("Current Max Petals: ", current_max_petals, " Available: ", petals_list[current_max_petals])


def farming_sonnenblumen_if_necessary():
    _need_stock = get_world_size() * get_world_size() * 2
    _current_energy = num_items(Items.Power)

    if _current_energy < _need_stock:
        farming_sonnenblumen()

