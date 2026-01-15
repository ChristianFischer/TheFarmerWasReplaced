from __builtins__ import *
import boundaries
import job_drones
import lib_farming
import movement
import unlocks


def farming_pumpkins():
    job_drones.spawn_multi(farming_pumpkins_proc)
    harvest()


def farming_pumpkins_proc(bounds, _parameters={}):
    pumpkin_cost = get_cost(Entities.Pumpkin)

    while unlocks.is_all_available(pumpkin_cost):
        boundaries.move_to_origin(bounds)
        finished = True

        dead_pumpkins_zone = boundaries.make_invalid_bounds()

        while True:
            entity = get_entity_type()
            is_invalid = False

            if entity == Entities.Dead_Pumpkin:
                lib_farming.do_plant(Entities.Pumpkin)
                is_invalid = True
            elif entity != Entities.Pumpkin:
                harvest()
                lib_farming.do_plant(Entities.Pumpkin)
                is_invalid = True
            else:
                # pumpkins are invalid if still growing
                if not can_harvest():
                    is_invalid = True

            if is_invalid:
                lib_farming.do_watering()

                dead_pumpkins_zone = boundaries.expand(
                    dead_pumpkins_zone,
                    get_pos_x(), get_pos_y()
                )

                finished = False

            if movement.fly_field_step_in_bounds(bounds):
                break

        if finished:
            break

        bounds = dead_pumpkins_zone

