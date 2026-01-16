from __builtins__ import *
import boundaries
import lib_farming
import movement


def farming_cactus():
    farming_cactus_plant()
    farming_cactus_sort()
    farming_cactus_harvest()


# step1: planting
def farming_cactus_plant():
    movement.reset_world_pos()
    while True:
        if get_entity_type() != Entities.Cactus:
            # erase any previous plant
            if can_harvest():
                harvest()

            lib_farming.do_plant(Entities.Cactus)

        if movement.fly_field_step():
            break


# step2: sorting
def farming_cactus_sort():
    bounds = boundaries.make_world_bounds()
    max_size = get_world_size() - 1
    fly_reverse = False
    is_sorted = False

    boundaries.move_to_origin(bounds)

    while not is_sorted:
        unsorted_area = None
        is_sorted = True

        while True:
            cactus_size = measure()
            invalidate_area = None
            x = get_pos_x()
            y = get_pos_y()

            if x > 0 and cactus_size < measure(West):
                swap(West)
                invalidate_area = boundaries.make_bounds_capped(x - 2, y + 1, x + 1, y - 1, max_size)
                cactus_size = measure()

            if y > 0 and cactus_size < measure(South):
                swap(South)
                invalidate_area = boundaries.make_bounds_capped(x - 1, y + 1, x + 1, y - 2, max_size)

            if invalidate_area != None:
                if unsorted_area == None:
                    unsorted_area = invalidate_area
                else:
                    unsorted_area = boundaries.merge(unsorted_area, invalidate_area)
                is_sorted = False

            if fly_reverse:
                if movement.fly_field_step_in_bounds_reverse(bounds):
                    break
            else:
                if movement.fly_field_step_in_bounds(bounds):
                    break

        fly_reverse = not fly_reverse
        bounds = unsorted_area


# step3: harvest
def farming_cactus_harvest():
    while can_harvest() == False:
        do_a_flip()

    harvest()

