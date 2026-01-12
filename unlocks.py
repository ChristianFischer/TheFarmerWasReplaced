current_unlock_index = 0
unlock_list = [
    (Unlocks.Expand, 5),
    (Unlocks.Watering, 5),
    (Unlocks.Speed, 5),
    (Unlocks.Grass, 5),
    (Unlocks.Trees, 5),
    (Unlocks.Carrots, 5),
    (Unlocks.Pumpkins, 5),
    (Unlocks.Mazes, 1),
    (Unlocks.Expand, 7),
    (Unlocks.The_Farmers_Remains, 1),
    (Unlocks.Top_Hat, 1),
]


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
            continue

        # return the next unlockable and it's costs
        return unlock_item, costs
