def get_plant_for(need):
    if need == Items.Carrot:
        return Entities.Carrot
    elif need == Items.Wood:
        if (get_pos_x() + get_pos_y()) % 2 == 1:
            return Entities.Tree
        return Entities.Bush
    elif need == Items.Hay:
        return Entities.Grass
    elif need == Items.Pumpkin:
        return Entities.Pumpkin
    elif need == Items.Power:
        return Entities.Sunflower
    elif need == Items.Cactus:
        return Entities.Cactus
    return None


def need_till_for(plant):
    if plant == Entities.Carrot:
        return True
    if plant == Entities.Pumpkin:
        return True
    if plant == Entities.Cactus:
        return True
    return False


def need_untill_for(plant):
    if plant == Entities.Grass:
        return True
    return False

    
def requires_ground_for(plant):
    if plant in [Entities.Grass]:
        return [Grounds.Grassland]
    if plant in [Entities.Carrot, Entities.Pumpkin, Entities.Sunflower, Entities.Cactus]:
        return [Grounds.Soil]
    return [Grounds.Grassland, Grounds.Soil]
        