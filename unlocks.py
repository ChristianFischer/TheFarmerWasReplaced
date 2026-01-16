from __builtins__ import *

current_unlock_index = 0
unlock_list = [
    (Unlocks.Speed, 1),
    (Unlocks.Expand, 1),
    (Unlocks.Grass, 2),
    (Unlocks.Plant, 1),
    (Unlocks.Hats, 1),

    (Unlocks.Expand, 2),
    (Unlocks.Speed, 2),
    (Unlocks.Fertilizer, 1),

    (Unlocks.Carrots, 1),
    (Unlocks.Expand, 4),
    (Unlocks.Speed, 3),

    (Unlocks.Watering, 1),
    (Unlocks.Trees, 1),
    (Unlocks.Sunflowers, 1),
    (Unlocks.Pumpkins, 1),
    (Unlocks.Cactus, 1),
    (Unlocks.Fertilizer, 1),
    (Unlocks.Mazes, 1),
    (Unlocks.Dinosaurs, 1),

    (Unlocks.Expand, 5),
    (Unlocks.Polyculture, 1),
    (Unlocks.Megafarm, 2),
    (Unlocks.Trees, 3),
    (Unlocks.Pumpkins, 3),
    (Unlocks.Cactus, 3),
    (Unlocks.Mazes, 3),
    (Unlocks.Dinosaurs, 3),

    (Unlocks.Watering, 5),
    (Unlocks.Speed, 4),
    (Unlocks.Grass, 4),
    (Unlocks.Trees, 4),
    (Unlocks.Carrots, 4),
    (Unlocks.Pumpkins, 4),

    (Unlocks.Expand, 5),
    (Unlocks.Watering, 5),
    (Unlocks.Speed, 5),
    (Unlocks.Grass, 5),
    (Unlocks.Trees, 5),
    (Unlocks.Carrots, 5),
    (Unlocks.Pumpkins, 5),
    (Unlocks.Fertilizer, 1),
    (Unlocks.Mazes, 1),
    (Unlocks.Fertilizer, 4),
    (Unlocks.Expand, 7),

    (Unlocks.Polyculture, 4),
    (Unlocks.Grass, 9),
    (Unlocks.Carrots, 9),
    (Unlocks.Trees, 9),
    (Unlocks.Pumpkins, 9),
    (Unlocks.Cactus, 5),
    (Unlocks.Mazes, 5),

    (Unlocks.Polyculture, 4),
    (Unlocks.Grass, 10),
    (Unlocks.Carrots, 10),
    (Unlocks.Trees, 10),
    (Unlocks.Pumpkins, 10),
    (Unlocks.Cactus, 6),
    (Unlocks.Mazes, 6),
    (Unlocks.Dinosaurs, 6),

    # leaderboard finished here
    (Unlocks.Leaderboard, 1),

    (Unlocks.Top_Hat, 1),
    (Unlocks.The_Farmers_Remains, 1),
]


all_available_plants = None


def is_all_available(costs):
    for costs_item in costs:
        if num_items(costs_item) < costs[costs_item]:
            return False
    return True


def find_next_unlock():
    global current_unlock_index
    global unlock_list

    max_unlock_index = len(unlock_list)

    while True:
        # stop if finished the list
        if current_unlock_index >= max_unlock_index:
            return None

        unlock_item, level = unlock_list[current_unlock_index]

        # switch to next list entry, if the current one is already unlocked
        if num_unlocked(unlock_item) >= level:
            current_unlock_index = current_unlock_index + 1
            continue

        # buy the current unlock, if possible
        costs = get_cost(unlock_item)
        if is_all_available(costs):
            unlock(unlock_item)

            # invalidate list
            global all_available_plants
            all_available_plants = None

            continue

        # return the next unlockable and it's costs
        return unlock_item, costs


def get_all_available_plants():
    global all_available_plants

    if all_available_plants == None:
        all_available_plants = {
            Items.Hay: num_unlocked(Unlocks.Grass),
            Items.Wood: num_unlocked(Unlocks.Trees),
        }

        unlocks_carrots = num_unlocked(Unlocks.Carrots)
        unlocks_pumpkins = num_unlocked(Unlocks.Pumpkins)
        unlocks_cactus = num_unlocked(Unlocks.Cactus)
        unlocks_sunflowers = num_unlocked(Unlocks.Sunflowers)
        unlocks_mazes = num_unlocked(Unlocks.Mazes)
        unlocks_dinosaurs = num_unlocked(Unlocks.Dinosaurs)

        if unlocks_carrots > 0:
            all_available_plants[Items.Carrot] = unlocks_carrots

        if unlocks_pumpkins > 0:
            all_available_plants[Items.Pumpkin] = unlocks_pumpkins

        if unlocks_cactus > 0:
            all_available_plants[Items.Cactus] = unlocks_cactus

        if unlocks_sunflowers > 0:
            all_available_plants[Items.Power] = unlocks_sunflowers

        if unlocks_mazes > 0:
            all_available_plants[Items.Gold] = unlocks_mazes

        if unlocks_dinosaurs > 0:
            all_available_plants[Items.Bone] = unlocks_dinosaurs


    return all_available_plants
