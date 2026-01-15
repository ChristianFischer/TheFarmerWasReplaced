from __builtins__ import *
import boundaries
import demands
import job_drones
import lib_farming
import movement
import plants


max_sunflower_petal = 0
companion_wishlist = {}


def reset_companion_wishlist():
    global companion_wishlist
    companion_wishlist = {}


def farm(current_demand, fertilize=False):
    job_drones.spawn_multi(farm_in_bounds, {"current_demand": current_demand, "fertilize": fertilize})


def farm_in_bounds(bounds, parameters):
    current_demand = parameters["current_demand"]
    fertilize = parameters["fertilize"]

    global max_sunflower_petal
    global companion_wishlist

    handle_companions = demands.can_use_companions(current_demand)

    if max_sunflower_petal > 7:
        max_sunflower_petal -= 1

    boundaries.move_to_origin(bounds)

    while True:
        current_position = (get_pos_x(), get_pos_y())

        if can_harvest():
            if get_entity_type() == Entities.Sunflower:
                petals = measure()
                if petals >= max_sunflower_petal:
                    max_sunflower_petal = 0
                    harvest()
            else:
                harvest()

        to_plant = None

        # check if there's a demand for a specific companion plant
        if handle_companions and current_position in companion_wishlist:
            to_plant = companion_wishlist[current_position]
            companion_wishlist.pop(current_position)

        # otherwise take the current priority plant
        if to_plant == None:
            to_plant = plants.get_plant_for(current_demand)

        if to_plant != Entities.Grass:
            lib_farming.do_plant(to_plant)

            if to_plant == Entities.Sunflower and get_entity_type() == Entities.Sunflower:
                petals = measure()
                max_sunflower_petal = max(max_sunflower_petal, petals)

            # store any demand for a companion plant
            if handle_companions:
                wish = get_companion()
                if wish != None:
                    wish_position = wish[1]
                    wish_item = wish[0]

                    companion_wishlist[wish_position] = wish_item

            lib_farming.do_watering()

            if fertilize:
                lib_farming.do_fertilize()
        else:
            if get_ground_type() == Grounds.Soil:
                till()

        if movement.fly_field_step_in_bounds(bounds):
            break
