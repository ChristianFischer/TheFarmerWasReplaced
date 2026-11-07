from __builtins__ import *
import boundaries
import job_drones
import movement


def farming_rice(demand_amount):
    current_demand = Items.Rice

    while True:
        # when already below surface, reset the world first
        if get_pos_z() < 0:
            clear()

        # at first, dig to the first layer of clay
        job_drones.spawn_multi(
            get_to_clay_job_entry,
            { }
        )

        # now start planting / harvesting
        job_drones.spawn_multi(
            farm_rice_in_bounds_job_entry,
            {
                "current_demand": current_demand,
                "demand_amount": demand_amount,
            }
        )

        # stop if either no demand was specified or already fulfilled
        if demand_amount == None or num_items(current_demand) >= demand_amount:
            break




def get_to_clay_job_entry(bounds, parameters):
    _ = parameters
    return get_to_clay(bounds)


def get_to_clay(bounds):
    if bounds != None:
        boundaries.move_to_origin(bounds)
    else:
        movement.reset_world_pos()

    while True:
        clay_found = False

        while True:
            # always harvest coal
            if get_ground_type() == Grounds.Coal:
                dig()
            # dig in checker pattern to get faster; remaining blocks will collapse
            elif (get_pos_x() + get_pos_y()) % 2 == 0:
                dig()

            # Check if clay is found
            if get_ground_type() == Grounds.Clay:
                clay_found = True

            if bounds != None:
                if movement.fly_field_step_in_bounds(bounds):
                    break
            else:
                if movement.fly_field_step():
                    break

        if bounds != None:
            boundaries.move_to_origin(bounds)
        else:
            movement.reset_world_pos()

        if clay_found:
            break




def farm_rice_in_bounds_job_entry(bounds, parameters):
    current_demand = parameters["current_demand"]
    demand_amount = parameters["demand_amount"]
    return farm_rice_in_bounds(bounds, current_demand, demand_amount)



def farm_rice_in_bounds(bounds, current_demand, demand_amount):
    if bounds != None:
        boundaries.move_to_origin(bounds)
    else:
        movement.reset_world_pos()

    while True:
        any_rice_field = False

        while True:
            current_ground = get_ground_type()

            # plant on clay
            if current_ground == Grounds.Clay:
                plant(Entities.Rice)
                any_rice_field = True

            # harvest
            elif current_ground == Grounds.Rice_Terrace:
                if get_entity_type() == Entities.Rice:
                    if can_harvest():
                        harvest()

                plant(Entities.Rice)

            # harvest
            elif current_ground == Grounds.Dry_Rice_Terrace:
                if get_entity_type() == Entities.Rice:
                    if can_harvest():
                        harvest()
                        dig()

                any_rice_field = True

            # ignore rock, we won't dig any deeper
            elif current_ground == Grounds.Rock:
                pass

            # dig everything else
            else:
                dig()

            if bounds != None:
                if movement.fly_field_step_in_bounds(bounds):
                    break
            else:
                if movement.fly_field_step():
                    break

        if bounds != None:
            boundaries.move_to_origin(bounds)
        else:
            movement.reset_world_pos()

        if not any_rice_field:
            break
