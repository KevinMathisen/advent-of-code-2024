def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    lines = list(content.strip().split("\n"))

    boxes = set()
    start_pos = []
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == '#':
                boxes.add((x, y))
            
            elif lines[y][x] == '^':
                start_pos = (x, y)
            
    bounds = {
        "min_y": 0,
        "max_y": len(lines)-1,
        "min_x": 0,
        "max_x": len(lines[0])-1
    }

    return start_pos, boxes, bounds

def print_map(visited_positions, bounds, boxes, current_x, current_y):    
    for y in range(bounds["min_y"], bounds["max_y"] + 1):
        line = ""
        for x in range(bounds["min_x"], bounds["max_x"] + 1):
            if (x, y) == (current_x, current_y):
                line += "^"  # Current position
            elif (x, y) in visited_positions:
                line += "o"  # Visited position
            elif (x, y) in boxes:
                line += "#"  # Box
            else:
                line += "."  # Empty space
        print(line)
    print("\n" + "-" * (bounds["max_x"] - bounds["min_x"] + 1) + "\n")

def print_map_2(visited_positions, bounds, boxes, new_box):
    visited_pos = next(iter(visited_positions))
    if len(visited_pos) == 3:
        new_visited_pos = set()
        for pos in visited_positions:
            new_visited_pos.add((pos[0], pos[1]))
        visited_positions = new_visited_pos
    
    for y in range(bounds["min_y"], bounds["max_y"] + 1):
        line = ""
        for x in range(bounds["min_x"], bounds["max_x"] + 1):
            if (x, y) == new_box:
                line += "X"  # New box placement
            elif (x, y) in visited_positions:
                line += "o"  # Visited position
            elif (x, y) in boxes:
                line += "#"  # Box
            else:
                line += "."  # Empty space
        print(line)
    print("\n" + "-" * (bounds["max_x"] - bounds["min_x"] + 1) + "\n")



def perform_turn(x, y, direction, directions, boxes, bounds):
    # returns new location, which is -1, -1 if exited bounds
    # also returns direction (0, 1, 2, 3) corresponding to directions
    dx, dy = directions[direction]

    next_x = x + dx
    next_y = y + dy
    
    # Check if we are heading out of map, if so return -1 -1
    if next_x < bounds["min_x"] or next_x > bounds["max_x"] or next_y < bounds["min_y"] or next_y > bounds["max_y"]:
        return -1, -1, -1

    # Check if we need to turn, if so change direction (until no longer obstacle in front)
    while (next_x, next_y) in boxes:
        direction = (direction+1)%4
        dx, dy = directions[direction]
        next_x = x + dx
        next_y = y + dy

    # Move in direction
    return next_x, next_y, direction

# Task 1
def task1(start_pos, boxes, bounds, directions):
    visited_positions = set()

    visited_positions.add(start_pos)
    x, y = start_pos
    direction = 0 # Corresponding to initial looking north

    # Perform turns until guard walks outside of map, saving the guards position underways
    while (x, y) != (-1, -1):
        x, y, direction = perform_turn(x, y, direction, directions, boxes, bounds)
        visited_positions.add((x, y))
        #print_map(visited_positions, bounds, boxes, x, y)

    return len(visited_positions)-1


# Task 2
def task2(start_pos, boxes, bounds, directions):
    # Need to try placing boxes
    # For each box we place, we need to simulate the new path
    # If the new path eventually visits the same coordinates as previous, 
    # AND in the same direction, then we have trapped the guard in a loop
    visited_positions = set()

    x, y = start_pos
    direction = 0 # Corresponding to initial looking north
    
    # Find the intial path to narrow down places where we try to place boxes
    # As we only need to consider boxes placed in the initial path, as these are the ones which will modify the path
    while (x, y) != (-1, -1):
        x, y, direction = perform_turn(x, y, direction, directions, boxes, bounds)
        
        # Save positions
        if (x, y) != (-1, -1):
            visited_positions.add((x, y))
    
    amount_loop_causing_boxes = 0

    # Check all possible placements of boxes
    for (org_x, org_y) in visited_positions:
        # Add the box to the map
        modified_boxes = boxes.copy()
        modified_boxes.add((org_x, org_y))

        visited_positions_2 = set()
        direction = 0
        prev_x, prev_y = start_pos
        x, y = prev_x, prev_y

        # Simulate the path of the guard until they exit or get stuck in a loop
        while (x, y) != (-1, -1):
            x, y, direction = perform_turn(x, y, direction, directions, modified_boxes, bounds)

            # Check if we previously have walked in the same direction. If so we are in a loop.
            if (prev_x, prev_y, direction) in visited_positions_2:
                amount_loop_causing_boxes += 1
                # print_map_2(visited_positions_2, bounds, boxes, (org_x, org_y))
                break

            # Save the previous position with the direction we headed in,
            #  and if we later get an overlap we have found a loop
            visited_positions_2.add((prev_x, prev_y, direction))
            prev_x, prev_y = x, y

    return amount_loop_causing_boxes


test = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

useTestInput = False
start_pos, boxes, bounds = readInput(useTestInput, test)

directions = [
    (0, -1),   # north
    (1, 0),   # east
    (0, 1),  # south
    (-1, 0)   # west
]

print(task1(start_pos, boxes, bounds, directions))

print(task2(start_pos, boxes, bounds, directions))