import movement


def handle(plant):
    if plant == Items.Pumpkin:
        while num_items(Items.Carrot) > 1 and  replace_dead_pumpkins():
            pass
    if plant == Items.Cactus:
        sort_cactus()
     
            
def replace_dead_pumpkins():
    found_any = False
    found_other = False
    while not movement.fly_over_field():
        entity = get_entity_type()
        if entity == Entities.Dead_Pumpkin:
            plant(Entities.Pumpkin)
            found_any = True
        elif entity != Entities.Pumpkin:
            found_other = True
    return found_any and not found_other
           
    
    
def sort_cactus():
    max_pos = get_world_size() - 1
    is_sorted = False
    
    while not is_sorted:
        is_sorted = True
        while True:
            if get_entity_type() != Entities.Cactus:
                return
        
            current_size = measure()
            
            if get_pos_x() > 0:
                west_size = measure(West)
                if west_size > current_size:
                    current_size = west_size
                    is_sorted = False
                    swap(West)
                
            if get_pos_y() < max_pos:
                north_size = measure(North)
                if north_size < current_size:
                    current_size = north_size
                    is_sorted = False
                    swap(North)
            
            if movement.fly_over_field():
                break
                    
    harvest()