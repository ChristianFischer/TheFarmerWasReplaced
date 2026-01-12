import lib_maze
import plants
import unlocks

all_items = [
    Items.Power,
    Items.Hay,
    Items.Wood,
    Items.Carrot,
    Items.Pumpkin,
    Items.Cactus,
    Items.Gold,
]


def find_demand():
    if num_items(Items.Power) < 1000:
        return Items.Power
    min_stock = 100
    for i in all_items:
        if num_items(i) < min_stock:
            return i

    next_unlock = unlocks.find_next_unlock()
    if next_unlock != None:
        cost_item = find_first_unavailable_costs(next_unlock[1], 1)
        if cost_item != None:
            return cost_item

    return all_items[len(all_items)-1]


def find_first_unavailable_costs_for(item, q):
    costs = get_cost(item)
    return find_first_unavailable_costs(costs, q)


def find_first_unavailable_costs(costs, q):
    for cost_item in costs:
        if num_items(cost_item) < costs[cost_item] * q:
            return cost_item

    return None


def compute_maze_costs():
    return {
        Items.Weird_Substance: lib_maze.calc_required_substance(),
        Items.Hay: 1000,
    }


def find_next_required_item():
    min_amount_plant = get_world_size() * get_world_size()
    demand_item = find_demand()

    # to collect gold from mazes, we need Weird Substance to create the maze
    if demand_item == Items.Gold:
        maze_costs = find_first_unavailable_costs(compute_maze_costs(), 1)
        if maze_costs != None:
            demand_item = maze_costs

    # if weird substance is required, request another item instead plus fertilization
    if demand_item == Items.Weird_Substance:
        return Items.Wood, True

    while True:
        demand_plant = plants.get_plant_for(demand_item)
        if demand_plant == None:
            break
        costs_item = find_first_unavailable_costs_for(demand_plant, min_amount_plant)
        if costs_item == None:
            break
        demand_item = costs_item

    return demand_item, False


def can_use_companions(plant):
    possible_plants = {Items.Hay, Items.Wood, Items.Carrot}
    if plant in possible_plants:
        return True
    else:
        return False