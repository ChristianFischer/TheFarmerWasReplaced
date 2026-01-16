from __builtins__ import *
import movement
import demands
import farming
import farming_cactus
import farming_dinos
import farming_pumpkins
import farming_sonnenblumen
import maze


last_demand = None
current_demand = None


if num_unlocked(Unlocks.Hats):
    change_hat(Hats.Brown_Hat)


# if we're still inside a maze, erase it
if get_entity_type() == Entities.Hedge:
    harvest()


movement.reset_world_pos()


while True:
    last_demand = current_demand
    current_demand, demand_fertilizer = demands.find_next_required_item()
    handle_fertilization = False
    companion_wishlist = {}

    if last_demand != current_demand:
        farming.reset_companion_wishlist()

    if current_demand == Items.Gold:
        maze.run_maze()
    elif current_demand == Items.Power:
        farming_sonnenblumen.farming_sonnenblumen(demand_fertilizer)
    elif current_demand == Items.Pumpkin:
        farming_pumpkins.farming_pumpkins()
    elif current_demand == Items.Cactus:
        farming_cactus.farming_cactus()
    elif current_demand == Items.Bone:
        farming_dinos.farming_dinosaur()
    else:
        farming.farm(current_demand, demand_fertilizer)

