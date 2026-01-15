from __builtins__ import *
import boundaries
import movement


job_proc = None
job_bounds = None
job_parameters = {}

watering_drone_handle = None


def spawn_multi(proc, parameters={}):
    max_drone_count = max_drones()

    if max_drone_count == 1:
        bounds = boundaries.make_world_bounds()
        proc(bounds, parameters)
    else:
        world_bounds = boundaries.make_world_bounds()
        bounds_list = boundaries.split(world_bounds, max_drone_count)
        job_list = []

        # preserve one subfield for the current drone itself
        master_bounds = bounds_list.pop(0)

        # entry point to start the actual drone job
        def drone_job_start():
            global job_proc
            global job_bounds
            global job_parameters

            job_proc(job_bounds, job_parameters)

        global job_proc
        job_proc = proc

        # spawn a new drone for each area
        for bounds in bounds_list:
            global job_bounds
            global job_parameters
            job_bounds = bounds
            job_parameters = parameters

            drone = spawn_drone(drone_job_start)

            job_list.append(drone)

        # run the job for the current drone itself
        proc(master_bounds, parameters)
        boundaries.move_to_origin(world_bounds)

        # wait for all other drones to finish
        for drone in job_list:
            wait_for(drone)



def launch_watering_drone():
    if num_unlocked(Unlocks.Megafarm) == 0:
        return

    def job():
        change_hat(Hats.Green_Hat)

        while True:
            num_water = num_items(Items.Water)
            num_fields = get_world_size() ** 2

            if num_water > num_fields * 4:
                treshold = 0.75
            elif num_water > num_fields * 2:
                treshold = 0.5
            elif num_water > num_fields:
                treshold = 0.25
            else:
                return

            while not movement.fly_field_step():
                if get_ground_type() != Grounds.Soil:
                    continue
                if get_water() < treshold:
                    use_item(Items.Water)

    global watering_drone_handle
    if watering_drone_handle != None:
        has_finished(watering_drone_handle)
        watering_drone_handle = None

    if watering_drone_handle == None:
        watering_drone_handle = spawn_drone(job)
