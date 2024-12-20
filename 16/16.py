import heapq

def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    lines = list(content.strip().split("\n"))

    start_pos = (-1, -1)
    end_pos = (-1, -1)
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == 'S':
                start_pos = (x, y)
            if lines[y][x] == 'E':
                end_pos = (x, y)

    return lines, start_pos, end_pos

def print_map_with_direction(map, start_pos, end_pos, direction):
    # Create a copy of the map to modify for printing
    map_copy = [list(row) for row in map]

    # Define direction symbols
    direction_symbols = ['^', '>', 'v', '<']

    # Update the map with direction symbols
    for (x, y), dir_index in direction.items():
        if dir_index != -1:
            map_copy[y][x] = direction_symbols[dir_index]

    # Mark the start and end positions
    start_x, start_y = start_pos
    end_x, end_y = end_pos
    map_copy[start_y][start_x] = 'S'
    map_copy[end_y][end_x] = 'E'

    # Print the map
    for row in map_copy:
        print(''.join(row))
    print()

def print_map_with_distance(map, start_pos, end_pos, distance_from_start):
    margin = 6
    # Create a copy of the map to modify for printing
    map_copy = [list(row) for row in map]

    # Update the map with distances
    for (x, y), distance in distance_from_start.items():
        if distance != float('inf'):
            map_copy[y][x] = str(distance).rjust(margin)  # Right-align the distance with width of 5

    # Mark the start and end positions
    start_x, start_y = start_pos
    end_x, end_y = end_pos
    map_copy[start_y][start_x] = 'S'.rjust(margin)
    map_copy[end_y][end_x] = 'E'.rjust(margin)

    # Print the map with right-aligned characters
    for y in range(len(map_copy)):
        for x in range(len(map_copy[y])):
            if map_copy[y][x] not in {'S', 'E'} and not map_copy[y][x].strip().isdigit():
                map_copy[y][x] = map_copy[y][x].rjust(margin)
        print(''.join(map_copy[y]))
    print()

# Task 1
def task1(map, start_pos, end_pos, directions):
    # Want to find fastest way from start pos to end pot
    #  i.e. dijkstra 
    # Use priority queue, where we add neigbours with their current distance
    #  to start as their priority. 
    # Each round we chose the node with the lowest distance/highest priority. 
    #  Can calculate score to each neighbour, check if lower.
    #    If lower, update the nodes distance and update its priority score
    # Once the end node is the one with the highest priority and selected
    #   return this score. 
    # 
    
    # Contains priority (distance to start), coordinates
    priority_queue = []
    # Total distance from tiles to start
    distance_from_start = {(x, y): float('inf') for y in range(len(map)) for x in range(len(map[y])) if map[y][x] != '#'}
    # Direction of tile (0 = north, 1 = east, 2 = south, 3 = west)
    direction = {(x, y): -1 for y in range(len(map)) for x in range(len(map[y])) if map[y][x] != '#'}
    
    heapq.heappush(priority_queue, (0, start_pos, 1))
    distance_from_start[start_pos] = 0
    direction[start_pos] = 1 # Corresponding to east

    while priority_queue:
        current_distance, (x, y), current_direction = heapq.heappop(priority_queue)

        # If the tile reached is the end, its score is the lowest it can have
        if (x, y) == end_pos:
            print_map_with_direction(map, start_pos, end_pos, direction)
            print_map_with_distance(map, start_pos, end_pos, distance_from_start)
            return current_distance
        
        # If lower distance already found, we can ignore this tile 
        # Not neccessarily true, as the lower distance may come from different direction
        # Therfore need to check if this direction can give neighbours lower values
        # if distance_from_start[(x, y)] < current_distance:
        #     continue

        # Check each potential neighbour
        for i in range(len(directions)):
            dx, dy = directions[i]
            next_x, next_y = x+dx, y+dy
            
            # Check if valid neighbour
            if map[next_y][next_x] == '#':
                continue
            
            # Calculate turn penalty based on change of direction
            turn_penalty = 0
            if abs(i-current_direction) == 1 or abs(i-current_direction) == 3:
                turn_penalty = 1000
            elif abs(i-current_direction) == 2:
                turn_penalty = 2000

            # Calculate distance if walking via current tile
            new_distance = current_distance + turn_penalty + 1

            # If new score if worse than previous, dont update
            if new_distance >= distance_from_start[(next_x, next_y)]:
                continue

            # Update neighbour direction, its score, and add it to the queue
            direction[(next_x, next_y)] = i
            distance_from_start[(next_x, next_y)] = new_distance
            heapq.heappush(priority_queue, (new_distance, (next_x, next_y), i))

    print_map_with_direction(map, start_pos, end_pos, direction)

    # Gone trough all paths, and not found end
    return float('inf')


# Task 2
def task2(map, start_pos, end_pos, directions):
    
    pass

test1 = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""
test = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""

useTestInput = True
lines, start_pos, end_pos = readInput(useTestInput, test)

directions = [
    (0, -1),   # north
    (1, 0),   # east
    (0, 1),  # south
    (-1, 0)   # west
]

print(task1(lines, start_pos, end_pos, directions))

print(task2(lines, start_pos, end_pos, directions))