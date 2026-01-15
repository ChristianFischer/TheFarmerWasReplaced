import movement
from __builtins__ import *
import plants


def do_plant(_p):
    if not get_ground_type() in plants.requires_ground_for(_p):
        till()

    plant(_p)


def do_watering():
    if get_ground_type() == Grounds.Soil:
        if get_water() < 0.5 and num_items(Items.Water) >= 1:
            use_item(Items.Water)


def do_fertilize():
    if num_items(Items.Fertilizer) > 0:
        if num_items(Items.Weird_Substance) > 0:
            if get_pos_x() % 3 == 1 and get_pos_y() % 3 == 1 and get_entity_type() != Entities.Bush:
                use_item(Items.Fertilizer)
                use_item(Items.Weird_Substance)
        else:
            use_item(Items.Fertilizer)


def fertilize_field():
    num_fertilizers = num_items(Items.Fertilizer)

    if num_items(Items.Weird_Substance) >= num_fertilizers:
        movement.reset_world_pos()

        for _y in range(get_world_size()):
            if get_pos_y() % 3 == 1:
                for _x in range(get_world_size()):
                    if get_pos_x() % 3 == 1:
                        use_item(Items.Fertilizer)
                        use_item(Items.Weird_Substance)

                        # stop if out of fertilizers
                        num_fertilizers = num_fertilizers - 1
                        if num_fertilizers == 0:
                            return

                    move(East)

            move(South)

    elif num_items(Items.Fertilizer) >= all_fields:
        for _f in range(all_fields):
            movement.fly_field_step()
            use_item(Items.Fertilizer)

            # stop if out of fertilizers
            num_fertilizers = num_fertilizers - 1
            if num_fertilizers == 0:
                return
