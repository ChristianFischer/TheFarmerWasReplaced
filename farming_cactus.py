from __builtins__ import *
import lib_farming
import movement


def farming_cactus():
    farming_cactus_plant()
    farming_cactus_sort()
    farming_cactus_harvest()


# step1: planting
def farming_cactus_plant():
    for _f in range(get_world_size() * get_world_size()):
        if get_entity_type() != Entities.Cactus:
            # erase any previous plant
            if can_harvest():
                harvest()

            lib_farming.do_plant(Entities.Cactus)

        lib_farming.do_watering()

        movement.fly_over_field()

    movement.reset_world_pos()


# step2: sorting
def farming_cactus_sort():
    is_sorted = False
    while not is_sorted:
        is_sorted = True

        for _f in range(get_world_size() * get_world_size()):
            cactus_size = measure()
            if get_pos_x() > 0 and cactus_size < measure(West):
                swap(West)
                is_sorted = False
                cactus_size = measure()

            if get_pos_y() > 0 and cactus_size < measure(South):
                swap(South)
                is_sorted = False

            movement.fly_over_field()


# step3: harvest
def farming_cactus_harvest():
    while can_harvest() == False:
        do_a_flip()

    harvest()

