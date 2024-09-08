from __builtins__ import *
from farming_sonnenblumen import *
from lib_farming import *

primary = select_primary_plant()
max_sunflower_petal = 0
companion_wishlist = {}


while True:
    iterate_through_world()
    current_position = (get_pos_x(), get_pos_y())

    if get_pos_x() == 0 and get_pos_y() == 0:
        do_shopping()
        farming_sonnenblumen_if_necessary()
        primary = select_primary_plant()

    if can_harvest():
        if get_entity_type() == Entities.Sunflower:
            petals = measure()
            if petals >= max_sunflower_petal:
                max_sunflower_petal = 0
                harvest()
        else:
            harvest()

    p = None

    # check if there's a demand for a specific companion plant
    if current_position in companion_wishlist:
        p = companion_wishlist[current_position]

    # otherwise take the current priority plant
    if p == None:
        p = get_intended_plant(primary)

    # plant if different to the current entity
    if get_entity_type() != p:
        do_plant(p)

        if p == Entities.Sunflower:
            petals = measure()
            max_sunflower_petal = max(max_sunflower_petal, petals)

        # store any demand for a companion plant
        wish = get_companion()
        if wish != None:
            wish_position = (wish[1], wish[2])
            wish_item = wish[0]

            companion_wishlist[wish_position] = wish_item

        # erase demand for the currently planted field
        if current_position in companion_wishlist:
            companion_wishlist.pop(current_position)

    do_watering()
