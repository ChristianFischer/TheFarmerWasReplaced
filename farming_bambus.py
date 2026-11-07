from __builtins__ import *
import boundaries
import job_drones
import movement


def farming_bambus(demand_amount):
    current_demand = Items.Bamboo

    # when below surface, reset the world first
    if get_pos_z() < 0:
        clear()

    while True:
        job_drones.spawn_multi(
            farm_bambus_in_bounds_job_entry,
            {
                "current_demand": current_demand,
                "demand_amount": demand_amount,
            }
        )

        # stop if either no demand was specified or already fulfilled
        if demand_amount == None or num_items(current_demand) >= demand_amount:
            break




def farm_bambus_in_bounds_job_entry(bounds, parameters):
    current_demand = parameters["current_demand"]
    demand_amount = parameters["demand_amount"]
    return farm_bambus_in_bounds(bounds, current_demand, demand_amount)



def farm_bambus_in_bounds(bounds, current_demand, demand_amount):
    is_already_planted = False

    if bounds != None:
        origin   = boundaries.get_origin(bounds)
        size     = boundaries.get_size(bounds)
        origin_x = origin[0]
        origin_y = origin[1]
        size_x   = size[0]
        size_y   = size[1]
    else:
        origin_x = 0
        origin_y = 0
        size_x   = get_world_size()
        size_y   = get_world_size()

    num_rows      = size_x // 2     # number of rows to be planted
    num_row_steps = size_y - 2      # number of steps to be done each row

    while True:
        # Step 1: Planting
        if not is_already_planted:
            # start at origin, already first step into the row
            movement.move_to_no_wrap(origin_x, origin_y + 1)

            for x in range(num_rows):
                move(East)

                if x % 2 == 0:
                    current_dir = North
                else:
                    current_dir = South

                for y in range(num_row_steps):
                    if y != 0:
                        move(current_dir)

                    till()
                    plant(Entities.Bamboo)

                move(East)

            move(South)

            is_already_planted = True

        # back to origin
        movement.move_to_no_wrap(origin_x, origin_y)

        # Step 2: Cut fruits 3 times
        for _ in range(3):
            movement.move_to_no_wrap(origin_x, origin_y)

            # iterate over each column
            for x in range(num_rows):
                if x % 2 == 0:
                    current_dir = North
                else:
                    current_dir = South

                # iterate over each y coordinate, except the first one,
                # because we have to leave that one free as a passage
                for _y in range(num_row_steps):
                    move(current_dir)

                    bamboo_height = measure(East)
                    hover(bamboo_height)

                    # cut and back
                    move(East)
                    move(West)

                # move another step, which brings us into the corridor of the
                # next drone, or wraps around
                move(current_dir)

                if x != num_rows - 1:
                    move(East)
                    move(East)

        # Step 3: Harvest everything
        hover(1)
        movement.move_to_no_wrap(origin_x + 1, origin_y + 1)

        for x in range(num_rows):
            if x != 0:
                move(East)

            if x % 2 == 0:
                current_dir = North
            else:
                current_dir = South

            for _y in range(num_row_steps):
                move(current_dir)

            move(East)

        move(South)

        # stop if either no demand was specified or already fulfilled
        if demand_amount == None or num_items(current_demand) >= demand_amount:
            break
