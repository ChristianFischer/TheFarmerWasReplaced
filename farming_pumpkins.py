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

    boundaries.move_to_origin(bounds)

    # plant first round
    while True:
        if get_entity_type() != Entities.Pumpkin:
            lib_farming.do_plant(Entities.Pumpkin)

        if movement.fly_field_step_in_bounds(bounds):
            break

    # replace all dead pumpkins until the whole field is valid
    while unlocks.is_all_available(pumpkin_cost):
        dead_pumpkins_zone = boundaries.make_invalid_bounds()
        finished = True

        current_pumpkin = 0
        current_pumpkin_size = 0

        boundaries.move_to_origin(bounds)

        while True:
            entity = get_entity_type()
            is_invalid = False

            if entity == Entities.Dead_Pumpkin:
                plant(Entities.Pumpkin)
                lib_farming.do_watering()
                is_invalid = True
            elif entity != Entities.Pumpkin:
                harvest()
                plant(Entities.Pumpkin)
                is_invalid = True
            else:
                # pumpkins are invalid if still growing
                if can_harvest():
                    pk = measure()
                    if pk == current_pumpkin:
                        current_pumpkin_size = current_pumpkin_size + 1
                        # 6x6 has the highest possible multiplier, so we can harvest early
                        if current_pumpkin_size >= 6:
                            finished = True
                            break
                    else:
                        current_pumpkin = pk
                        current_pumpkin_size = 1
                else:
                    lib_farming.do_watering()
                    is_invalid = True

            if is_invalid:
                current_pumpkin = 0
                dead_pumpkins_zone = boundaries.expand(
                    dead_pumpkins_zone,
                    get_pos_x(), get_pos_y()
                )

                finished = False

            step = movement.fly_field_step_in_bounds_with_state(bounds)
            if step == movement.Movement_Next_Row:
                current_pumpkin = 0
            elif step == movement.Movement_Done:
                break

        if finished:
            break

        bounds = dead_pumpkins_zone

