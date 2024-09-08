from __builtins__ import *
from farming_sonnenblumen import farming_sonnenblumen_if_necessary
from lib_farming import *


def farming_cactus():
    farming_cactus_plant()
    farming_cactus_sort()
    farming_cactus_harvest()


# step1: planting
def farming_cactus_plant():
    do_shopping()

    for _f in range(get_world_size() * get_world_size()):
        iterate_through_world()

        if get_entity_type() != Entities.Cactus:
            # erase any previous plant
            if can_harvest():
                harvest()

            do_plant(Entities.Cactus)

        do_watering()

    reset_world_pos()

# step2: sorting
def farming_cactus_sort():
    is_sorted = False
    while is_sorted == False:
        is_sorted = True

        for _f in range(get_world_size() * get_world_size()):
            iterate_through_world()

            cactus_size = measure()
            if get_pos_x() > 0 and cactus_size < measure(West):
                swap(West)
                is_sorted = False
                cactus_size = measure()

            if get_pos_y() > 0 and cactus_size < measure(South):
                swap(South)
                is_sorted = False


# step3: harvest
def farming_cactus_harvest():
    while can_harvest() == False:
        do_a_flip()

    harvest()



while True:
    farming_sonnenblumen_if_necessary()

    farming_cactus()
