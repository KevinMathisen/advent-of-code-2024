def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    lines = list(content.strip().split("\n"))

    bounds = {
        "min_y": 0,
        "max_y": len(lines)-1,
        "min_x": 0,
        "max_x": len(lines[0])-1
    }

    # Convert to ints for easier comparison
    map = [[int(num) for num in line] for line in lines]

    return map, bounds



# Task 1
def task1(map, bounds, directions):
    # For all possible trailheads (tiles at height 0) get the amount of unique reachable tops
    # Return the sum of unique tops for each trailhead
    return sum([len(get_reachable_tops(x, y, map, bounds, directions)) for y in range(len(map)) for x in range(len(map[y])) if map[y][x] == 0])

def get_reachable_tops(x, y, map, bounds, directions):
    # Traverse all paths, finding unique tops reachable from the current tile

    # Return location of top
    if map[y][x] == 9:
        return {(x, y)}
    
    # Try to move in all directions, saving the unique reachable tops from all directions
    reachable_tops = set()
    for (dx, dy) in directions:
        next_x, next_y = (x+dx, y+dy)
        if next_x < bounds["min_x"] or next_x > bounds["max_x"] or next_y < bounds["min_y"] or next_y > bounds["max_y"]:
            continue # Out of bounds
        if map[next_y][next_x] - map[y][x] == 1:
            # Possible path, as we increase height by one
            reachable_tops = reachable_tops.union(get_reachable_tops(next_x, next_y, map, bounds, directions))

    return reachable_tops 

# Task 2
def task2(map, bounds, directions):
    # For all possible trailheads (tiles at height 0) get the amount of possible paths
    # Return the sum of all possible paths
    return sum([len(get_all_paths(x, y, map, bounds, directions)) for y in range(len(map)) for x in range(len(map[y])) if map[y][x] == 0])

def get_all_paths(x, y, map, bounds, directions):
    # Traverse all paths, finding amount of paths leading to a top

    # Return location of top
    if map[y][x] == 9:
        return [(x, y)]
    
    # Try to move in all directions, saving the reachable tops from all directions
    paths = []
    for (dx, dy) in directions:
        next_x, next_y = (x+dx, y+dy)
        if next_x < bounds["min_x"] or next_x > bounds["max_x"] or next_y < bounds["min_y"] or next_y > bounds["max_y"]:
            continue # Out of bounds
        if map[next_y][next_x] - map[y][x] == 1:
            # Possible path, as we increase height by one
            paths.extend(get_all_paths(next_x, next_y, map, bounds, directions))

    return paths   

test = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

directions = [
    (0, -1),   # north
    (1, 0),   # east
    (0, 1),  # south
    (-1, 0)   # west
]

useTestInput = False
map, bounds = readInput(useTestInput, test)

print(task1(map, bounds, directions))

print(task2(map, bounds, directions))