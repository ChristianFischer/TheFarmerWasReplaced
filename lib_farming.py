from __builtins__ import *


def reset_world_pos():
    while get_pos_x() > 0:
        move(West)

    while get_pos_y() < (get_world_size() - 1):
        move(North)


def reset_world_pos_0():
    while get_pos_x() > 0:
        move(West)

    while get_pos_y() > 0:
        move(South)


def iterate_through_world():
    move(East)
    if get_pos_x() == 0:
        move(South)


def do_shopping():
    _seeds = [Items.Carrot_Seed, Items.Pumpkin_Seed, Items.Sunflower_Seed, Items.Cactus_Seed, Items.Fertilizer]
    _need_stock = get_world_size() * get_world_size() * 2

    for _s in _seeds:
        _stock = num_items(_s)

        if _stock < _need_stock:
            trade(_s, _need_stock - _stock)


def select_primary_plant():
    _basic_stock = 500

    if num_items(Items.Carrot) < _basic_stock:
        return Entities.Carrots
    if num_items(Items.Wood) < _basic_stock:
        return Entities.Tree
    if num_items(Items.Hay) < _basic_stock:
        return Entities.Grass

    if num_items(Items.Carrot) < 5000:
        return Entities.Carrots

    return Entities.Pumpkin


def get_intended_plant(_primary_plant):
    _x = get_pos_x()
    _y = get_pos_y()
    _max = get_world_size() - 1

    if _primary_plant != None:
        if _primary_plant == Entities.Tree:
            if (_x + _y) % 2 == 0:
                return Entities.Tree
            return Entities.Bush

        return _primary_plant

    return Entities.Grass


def get_intended_plant_0ld():
    _x = get_pos_x()
    _y = get_pos_y()
    _max = get_world_size() - 1

    if _x < 3 and _y > 0 and _y < 4:
        return Entities.Pumpkin

    if _x > 2 and _y < 2:
        if (_x + _y) % 2 == 0:
            return Entities.Tree
        return Entities.Bush

    if _x < 3:
        return Entities.Grass

    return Entities.Carrots


def requires_till(_p):
    return True


# if _p == Entities.Carrots:
#    return True
# if _p == Entities.Sunflower:
#    return True
# if _p == Entities.Pumpkin:
#    return True
# return False


def do_plant(_p):
    if requires_till(_p):
        if get_ground_type() == Grounds.Turf:
            till()

    plant(_p)


def do_watering():
    if get_ground_type() == Grounds.Soil:
        if get_water() < 0.5:
            use_item(Items.Water_Tank)
