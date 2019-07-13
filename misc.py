import copy

# Converts a string to a list of tiles
def string_to_tiles(str):
    # Base case
    if len(str) == 0:
        return []

    # Stores char in question
    char = str[0]

    # Stores what tile
    tile = char

    if len(str) >= 2 and char == 'q' and str[1] == 'u':
        # Recursive case (if it is qu)
        return ["qu"] + string_to_tiles(str[2:])
    else:
        # Recursive case
        return [tile] + string_to_tiles(str[1:])


# Converts a list of tiles to a string
def tiles_to_string(tiles):
    # Base case
    if len(tiles) == 0:
        return ""

    # Recursive case
    return ("q" if tiles[0] == "qu" else tiles[0]) + tiles_to_string(tiles[1:])


# Returns true if we can type out the tiles using this grid
def can_type(tiles_grid, tiles_word):
    # Base case; we can type this word
    if len(tiles_word) == 0:
        return True

    # Gets the tile to type out
    tile = tiles_word[0]

    # Check if we can type out this word
    if tile in tiles_grid:
        # Get the index in the grid
        index = tiles_grid.index(tile)

        # Recursive call
        return can_type(tiles_grid[:index] + tiles_grid[index + 1:], tiles_word[1:])

    # If there's some wildcard we can use instead
    if '?' in tiles_grid:
        # Get the index in the grid
        index = tiles_grid.index('?')

        # Recursive call
        return can_type(tiles_grid[:index] + tiles_grid[index + 1:], tiles_word[1:])

    # Base case; we can't type this word
    return False


# Converts a string to a list of tile positions, given a grid
def string_to_pos(grid, needle_string):
    # Base case
    if len(needle_string) == 0:
        return []

    # Gets the letter we are looking for
    needle_letter = needle_string[0]

    # Looks through the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):

            # If this letter is here
            if needle_letter == grid[i][j]:
                # Recursive case
                new_grid = copy.deepcopy(grid)
                new_grid[i][j] = None
                return [(i, j)] + string_to_pos(new_grid, needle_string[1:])

    # The letter is not here; look for a wildcard
    for i in range(len(grid)):
        for j in range(len(grid[i])):

            # If this letter is here
            if '?' == grid[i][j]:
                # Recursive case
                new_grid = copy.deepcopy(grid)
                new_grid[i][j] = None
                return [(i, j)] + string_to_pos(new_grid, needle_string[1:])

    # There is a problem
    raise Exception("Cannot type string " + needle_string + " because needle character " + needle_letter + " is not in the grid " + str(grid))