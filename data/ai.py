import copy
import random
import numpy as np


def list_of_rotated_pieces(piece):
    """ List all possible rotations of piece

        Function finds all possible rotations of
        a given piece, and returns them in a list.
    """
    pieces = [piece]
    temp_piece = copy.deepcopy(piece)
    for _ in range(3):
        rotated_piece = [list(y[::-1]) for y in zip(*temp_piece)]
        if rotated_piece not in pieces:
            pieces.append(rotated_piece)
        temp_piece = rotated_piece
    return pieces


def exist_arena(list_or_arenas, arena):
    """ Check is arena already exist

        Returns True if arena is in list_or_arenas,
        otherwise false.
    """
    for _, _, _, i in list_or_arenas:
        if arena == i:
            return False
    return True


def check_game_arena(arena, pos_x, pos_y, piece):
    """ Check game arena

        Check if given piece can be placed to given location
    """
    test_arena = copy.deepcopy(arena)
    try:
        for y, row in enumerate(piece):
            for x, cube in enumerate(row):
                # If there is a cube
                if cube:
                    if pos_x + x < 0 or test_arena[pos_y + y][pos_x + x]:
                        return False
                    test_arena[pos_y + y][pos_x + x] = cube
        return test_arena
    except IndexError:
        return False


def calculate_hole_count(arena):
    """ Count holes in arena """
    holes = 0
    for x in range(10):
        found_block = False
        for y in range(20):
            if found_block and not arena[y][x]:
                holes += 1
            else:
                if arena[y][x]:
                    found_block = True
    return holes


def calculate_added_shape_height(loc):
    """ New height on a piece """
    return 1 - loc[1]


def calculate_bumpiness(arena):
    """ Check bumpiness

        How bumpy is arena?
    """
    bump_sum = 0
    prev_bump = 20
    next_bump = 20
    for x in range(10):
        for y in range(20):
            next_bump = 20
            if arena[y][x]:
                next_bump = y
                break
        if x == 0:
            prev_bump = next_bump
            continue
        bump_sum += abs(next_bump - prev_bump)
        # print("x:", x, "next", next_bump, "prev", prev_bump)
        prev_bump = next_bump
    return bump_sum


def rate_arena(arena, loc):
    """ Rate arena

        Finds weight of given arena.
    """
    hole_count_multiplier = 10
    added_shape_height_multiplier = 0.5
    bumpiness_multiplier = 5

    hole_count = calculate_hole_count(arena)
    added_shape_height = calculate_added_shape_height(loc)
    bumpiness = calculate_bumpiness(arena)
    # print("holes", hole_count)
    # print("shape", added_shape_height)
    # print("bump", bumpiness)
    return hole_count_multiplier * hole_count + added_shape_height_multiplier * added_shape_height + bumpiness_multiplier * bumpiness


def play_ai(current_arena, current_piece):
    """ Play AI

        With current arena and current piece tries to figure
        out where to place that piece.
    """
    arenas = []
    arena = []

    for i, shape in enumerate(list_of_rotated_pieces(current_piece)):
        for pos_x in range(-1, 10):
            loc = (-1, -1)
            for pos_y in range(1, 20):
                appended_arena = check_game_arena(current_arena, pos_x, pos_y, shape)
                if not appended_arena:
                    break
                loc = (pos_x, pos_y)
                arena = appended_arena
            if not loc == (-1, -1) and exist_arena(arenas, arena):
                # print(loc)
                # print(np.array(arena))
                # print(rate_arena(arena, loc))
                arenas.append((loc, rate_arena(arena, loc), i, arena))

    min_locs = []
    min_weight = 1000
    for loc, weight, shape, arena in arenas:
        if weight < min_weight:
            min_locs = [(loc, shape, arena)]
            min_weight = weight
        elif weight == min_weight:
            min_locs.append((loc, shape, arena))
    c = random.choice(min_locs)
    # print()
    # print(np.array(c[2]))
    return c[0], c[1]


# Only for testing
# --------------------------------------------
i_shape = [
    [0, 0, 0, 0],
    [4, 4, 4, 4],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]
s_shape = [
    [0, 2, 2],
    [2, 2, 0],
    [0, 0, 0]
]

if __name__ == "__main__":
    game_arena = [[0 for _ in range(10)] for _ in range(20)]
    val = play_ai(game_arena, i_shape)
    print(val)
