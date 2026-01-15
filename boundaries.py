from __builtins__ import *
import movement


def make_bounds_capped(left, top, right, bottom, max_size):
    min_x = max(left, 0)
    max_x = min(right, max_size)
    min_y = max(bottom, 0)
    max_y = min(top, max_size)

    return [min_x, min_y, max_x, max_y]


def make_world_bounds():
    max_coordinate = get_world_size() - 1

    return [
        0,              # left
        0,              # bottom
        max_coordinate, # top
        max_coordinate, # right
    ]


def make_invalid_bounds():
    return [99999, 99999, 0, 0]


def get_origin(bounds):
    return bounds[0], bounds[1]


def get_path_end(bounds):
    height = bounds[3] - bounds[1] + 1
    if height%2 == 0:
        # even height, path ends left
        return bounds[0], bounds[3]
    else:
        # odd height, path ends right
        return bounds[2], bounds[3]


def expand(bounds, x, y):
    bounds[0] = min(bounds[0], x)
    bounds[1] = min(bounds[1], y)
    bounds[2] = max(bounds[2], x)
    bounds[3] = max(bounds[3], y)
    return bounds


def merge(a, b):
    min_x = min(a[0], b[0])
    min_y = min(a[1], b[1])
    max_x = max(a[2], b[2])
    max_y = max(a[3], b[3])
    return [min_x, min_y, max_x, max_y]


def move_to_origin(bounds):
    x, y = get_origin(bounds)
    movement.move_to(x, y)


def split(bounds, count):
    min_x, min_y, max_x, max_y = bounds
    width  = max_x - min_x + 1
    height = max_y - min_y + 1

    if count <= 1 or width <= 1 or height <= 1:
        return [bounds]

    if height > width:
        # split horizontally
        mid_y = (min_y + max_y) // 2
        a = [min_x, min_y,   max_x, mid_y]
        b = [min_x, mid_y+1, max_x, max_y]
    else:
        # split vertically
        mid_x = (min_x + max_x) // 2
        a = [min_x,   min_y, mid_x, max_y]
        b = [mid_x+1, min_y, max_x, max_y]

    # partition further
    if count > 2:
        count = count // 2
        a = split(a, count)
        b = split(b, count)

        return a + b
    else:
        return [a, b]
