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
    map_copy = [list(row) for row in map]
    direction_symbols = ['^', '>', 'v', '<']

    for (x, y), dir_index in direction.items():
        if dir_index != -1:
            map_copy[y][x] = direction_symbols[dir_index]

    map_copy[start_pos[1]][start_pos[0]] = 'S'
    map_copy[end_pos[1]][end_pos[0]] = 'E'

    for row in map_copy:
        print(''.join(row))
    print()

def print_map_with_distance(map, start_pos, end_pos, distance_from_start):
    margin = 6
    map_copy = [list(row) for row in map]

    for (x, y), distance in distance_from_start.items():
        if distance != float('inf'):
            map_copy[y][x] = str(distance).rjust(margin)

    map_copy[start_pos[1]][start_pos[0]] = 'S'.rjust(margin)
    map_copy[end_pos[1]][end_pos[0]] = 'E'.rjust(margin)

    for y in range(len(map_copy)):
        for x in range(len(map_copy[y])):
            if map_copy[y][x] not in {'S', 'E'} and not map_copy[y][x].strip().isdigit():
                map_copy[y][x] = map_copy[y][x].rjust(margin)
        print(''.join(map_copy[y]))
    print()

# Task 1
def task1(map, start_pos, end_pos, directions):
    # Want to find fastest way from start pos to end pos, i.e. dijkstra 

    # Contains priority (distance to start), coordinates
    priority_queue = [] # (<distance_to_start>, (<x>, <y>), <direction>)

    # Total distance from tiles to start ((<x>, <y>): <lowest_distance>)
    distance_from_start = {(x, y): float('inf') for y in range(len(map)) for x in range(len(map[y])) if map[y][x] != '#'}

    # Direction of tile (0 = north, 1 = east, 2 = south, 3 = west)
    direction = {(x, y): -1 for y in range(len(map)) for x in range(len(map[y])) if map[y][x] != '#'} # NB: not needed except for printing
    
    # Initialize queue, distance, and directions to start tile
    heapq.heappush(priority_queue, (0, start_pos, 1))
    distance_from_start[start_pos] = 0
    direction[start_pos] = 1 # Corresponding to east

    while priority_queue:
        # Get values for the next tile to evaluate as as long as there are more
        current_distance, (x, y), current_direction = heapq.heappop(priority_queue)

        # If the tile reached is the end, its score is the lowest it can have
        if (x, y) == end_pos:
            return current_distance, distance_from_start, direction
        
        # Next, evaluate the tile, i.e. its neighbours. Should be evaluated even if the tile previously has been evaluated, 
        #   as the tile may have a lower score and/or a different direction which needs to be evaluated
        for i in range(len(directions)):
            # Get the direction and coordiantes of each potential neighbour
            dx, dy = directions[i]
            next_x, next_y = x+dx, y+dy
            
            # Ignore walls, as they cant be traversed
            if map[next_y][next_x] == '#':
                continue
            
            # Calculate turn penalty based on change of direction to neighbour
            # Penalty is calculated by change of direction as follows: 0 degrees -> 0, 90 degrees -> 1000, 180 degrees -> 2000
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

    # Gone trough all paths and not found end
    return float('inf'), distance_from_start, direction


# Task 2
def task2(map, start_pos, end_pos, directions, distance_from_start_nodes, direction_nodes):
    # Want to find all paths which have the best cost from start to end. 
    # Can use resulting distance and direction map from task 1 to traverse best paths.
    # This can be achieved by traversing the map backwards, where we save the coordinates of all tiles in best paths
    # Return the size of the set.   

    path_heads = set() # Coordinates of where we currently are when travesing map
    path_tiles = set() # Coordiantes of all tiles visited in the best paths

    path_heads.add((end_pos, -1000)) # Start at end tile

    while len(path_heads) != 0:
        new_path_heads = set()
        # Go trough all divering best paths in path_head until there are no more paths to traverse:
        for (x, y), previous_direction in path_heads:
            # Save tile as a node visited
            path_tiles.add((x, y))
            
            # Check if reached start, if so path is finished
            if (x, y) == start_pos:
                continue

            # Add all best paths pointing to head as possible paths 
            for dx, dy in directions:
                next_x, next_y = x+dx, y+dy

                # If the neighbour is a wall, or does not have a distance defined, we do not consider it as potential best path
                if map[next_y][next_x] == '#' or distance_from_start_nodes[(next_x, next_y)] == float('inf'):
                    continue

                # Calculate values to compare the neighbour with the current head
                candidate_to_head_distance_difference = distance_from_start_nodes[(x, y)] - distance_from_start_nodes[(next_x, next_y)]
                direction_difference = abs(direction_nodes[(x, y)]-direction_nodes[(next_x, next_y)])
                direction_previous_difference = abs(previous_direction-direction_nodes[(next_x, next_y)])

                # Check if neighbour is one lower and same direction, if so we can add it as path head
                if candidate_to_head_distance_difference == 1 and direction_difference == 0:
                    new_path_heads.add(((next_x, next_y), direction_nodes[(x, y)]))
                
                # Also, if neighbour is 1001 lower, and 90 degrees difference direction, we can add it as path head
                elif candidate_to_head_distance_difference == 1001 and (direction_difference == 1 or direction_difference == 3):
                    new_path_heads.add(((next_x, next_y), direction_nodes[(x, y)]))

                # Also, if neighbour is 999 HIGHER, and it is the same direction as the previous head, add it as path head
                elif candidate_to_head_distance_difference == -999 and direction_previous_difference == 0:
                    new_path_heads.add(((next_x, next_y), direction_nodes[(x, y)]))
            
        path_heads = new_path_heads
                
    return len(path_tiles)


test = """
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

useTestInput = False
lines, start_pos, end_pos = readInput(useTestInput, test)

directions = [
    (0, -1),   # north
    (1, 0),   # east
    (0, 1),  # south
    (-1, 0)   # west
]
result_task_1, distance_from_start, direction_nodes = task1(lines, start_pos, end_pos, directions)

print(result_task_1)

print(task2(lines, start_pos, end_pos, directions, distance_from_start, direction_nodes))