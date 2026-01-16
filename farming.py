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


def farm(current_demand, demand_amount=None, fertilize=False):
    job_drones.spawn_multi(
            farm_in_bounds_job_entry,
            {
                "current_demand": current_demand,
                "demand_amount": demand_amount,
                "fertilize": fertilize
            }
    )


def farm_in_bounds_job_entry(bounds, parameters):
    current_demand = parameters["current_demand"]
    demand_amount = parameters["demand_amount"]
    fertilize = parameters["fertilize"]
    return farm_in_bounds(bounds, current_demand, demand_amount, fertilize)


def farm_in_bounds(bounds, current_demand, demand_amount, fertilize=False):
    global max_sunflower_petal
    global companion_wishlist

    handle_companions = demands.can_use_companions(current_demand)
    handle_watering = num_unlocked(Unlocks.Watering)

    if max_sunflower_petal > 7:
        max_sunflower_petal -= 1

    if bounds != None:
        boundaries.move_to_origin(bounds)
    else:
        movement.reset_world_pos()

    while True:
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

                if handle_watering:
                    lib_farming.do_watering()

                if fertilize:
                    lib_farming.do_fertilize()
            else:
                if get_ground_type() == Grounds.Soil:
                    till()

            if bounds != None:
                if movement.fly_field_step_in_bounds(bounds):
                    break
            else:
                if movement.fly_field_step():
                    break

        if demand_amount == None:
            break
        else:
            if bounds != None:
                boundaries.move_to_origin(bounds)
            else:
                movement.reset_world_pos()    
                
            if num_items(current_demand) >= demand_amount:
                break


def farm_simple(current_demand):
    return farm_simple_in_bounds(None, current_demand)


def farm_simple_in_bounds(bounds, current_demand):
    global companion_wishlist

    handle_companions = demands.can_use_companions(current_demand)
    handle_watering = num_unlocked(Unlocks.Watering)

    if bounds == None:
        area_size = get_world_size() ** 2
    else:
        area_size = boundaries.get_area(bounds)

    for _i in range(area_size):
        current_position = (get_pos_x(), get_pos_y())

        if can_harvest():
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

            # store any demand for a companion plant
            if handle_companions:
                wish = get_companion()
                if wish != None:
                    wish_position = wish[1]
                    wish_item = wish[0]

                    companion_wishlist[wish_position] = wish_item

            if handle_watering:
                lib_farming.do_watering()
        else:
            if get_ground_type() == Grounds.Soil:
                till()

        if bounds == None:
            movement.fly_field_step()
        else:
            movement.fly_field_step_in_bounds(bounds)
