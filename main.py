from __builtins__ import *
import movement
import demands
import farming
import farming_bambus
import farming_cactus
import farming_dinos
import farming_pumpkins
import farming_rice
import farming_sonnenblumen
import maze
import unlocks


last_demand = None
current_demand = None


if num_unlocked(Unlocks.Hats):
    change_hat(Hats.Brown_Hat)


# if we're still inside a maze, erase it
if get_entity_type() == Entities.Hedge:
    harvest()


movement.reset_world_pos()


# harvest grass until we're able to plant something else
while num_unlocked(Unlocks.Plant) == 0:
    for _i in range(get_world_size() ** 2):
        harvest()
        movement.fly_field_step()

    unlocks.find_next_unlock()


while True:
    last_demand = current_demand
    current_demand, demand_fertilizer = demands.find_next_required_item()

    if num_unlocked(Unlocks.Leaderboard) == 1:
        break

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
    elif current_demand == Items.Rice:
        farming_rice.farming_rice(None)
    elif current_demand == Items.Bamboo:
        farming_bambus.farming_bambus(None)
    else:
        #if num_unlocked(Unlocks.Expand) < 2:
        #    farming.farm_simple(current_demand)
        #else:
            farming.farm(current_demand, None, demand_fertilizer)

