import copy

def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    map_string, moves_string = list(content.strip().split("\n\n"))

    map = [list(map_line) for map_line in map_string.split("\n")]
    moves = ""
    moves_lines = moves_string.split("\n")
    for moves_line in moves_lines:
        moves += moves_line

    robot_position = (-1, -1)
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == '@':
                robot_position = (x, y)
                break

    return map, moves, robot_position

def print_map(map):
    for row in map:
        print(''.join(row))
    print()


# Task 1
def task1(map, moves, directions, robot_position):
    # Perform all moves by robot
    for move in moves:
        dx, dy = directions[move]
        robot_position = perform_move(robot_position, dx, dy, map)
    
    print_map(map)

    # Calculate the GPS cordinates for each box, and return sum of this
    return sum([ y*100+x for y in range(len(map)) for x in range(len(map[y])) if map[y][x] == 'O' ])

def perform_move(robot_position, dx, dy, map):
    # For each move, we need to check if it is possible. 
    #   Check this by checking if there are any available space in that direction
    #   Search stops when reached open space or when reached a wall.

    pushing = (-1, -1) # Only need to know location of last box to push
    tile = ''
    x, y = robot_position
    next_x, next_y = x, y

    # Continue searching in direction until we find an open space or a wall
    while tile != '#' and tile != '.':
        next_x, next_y = next_x+dx, next_y+dy
        tile = map[next_y][next_x]
        
        if tile == 'O': # Box to push
            pushing = (next_x, next_y)

    # If wall found before open space, robot cant move:
    if tile == '#':
        return robot_position
    
    # We have available space, move robot and all boxes in direction of move
    # Move box forward
    if pushing != (-1, -1):
        map[pushing[1]+dy][pushing[0]+dx] = 'O'
    # Move robot forward
    map[y][x] = '.' # Set previous position of robot to empty
    map[y+dy][x+dx] = '@' # Set new position of robot
    
    return (x+dx, y+dy) 

def create_wide_map(map):
    # Generate wide map, stretching everything except the robot
    new_map = []
    for line in map:
        new_line = []
        for tile in line:
            if tile == 'O': # Convert box to [ and ]
                new_line.append('[')
                new_line.append(']')
                continue

            new_line.append(tile) # Write all other tiles as same char
            if tile == '@':       # Robot should only be one, so only add empty
                new_line.append('.')
            else:                 # Other tiles should be stretched
                new_line.append(tile)

        new_map.append(new_line)

    # Find new robot position
    robot_position = (-1, -1)
    for y in range(len(new_map)):
        for x in range(len(new_map[y])):
            if new_map[y][x] == '@':
                robot_position = (x, y)
                break
    
    return new_map, robot_position 

# Task 2
def task2(map, moves, directions, robot_position):
    # Create new map
    map, robot_position = create_wide_map(map)

    # Perform all moves by robot
    for move in moves:
        dx, dy = directions[move]
        robot_position = perform_move_wide(robot_position, dx, dy, map)

    # Calculate the GPS cordinates for each box, and return sum of this
    return sum([ y*100+x for y in range(len(map)) for x in range(len(map[y])) if map[y][x] == '[' ])

def perform_move_wide(robot_position, dx, dy, map):
    pushing = [] # Coordinates of all part boxes which we want to push
    rob_x, rob_y = robot_position

    paths_coordinates = [] # Coordinates of the tiles we are evaluating
    paths_type = [] # Tile type we are evaluating

    # Start by appending first thing robot tries to move
    paths_coordinates.append((rob_x+dx, rob_y+dy))
    paths_type.append(map[rob_y+dy][rob_x+dx])

    # Continue searching in direction until we find all open spaces or any wall
    # Need to keep track of all states, and each round create new states based on these
    while '#' not in paths_type and ('[' in paths_type or ']' in paths_type):
        new_paths_coordinates = []
        new_paths_type = []
        # For each current tile/path, find the next ones to evaluate
        for i in range(len(paths_coordinates)):
            cur_x, cur_y = paths_coordinates[i]
            cur_type = paths_type[i]

            # if box already in pushing (as another box added it) we can ignore it
            if (cur_x, cur_y) in pushing:
                continue

            # Dont need to do anything if we have reached an open space or a wall
            if cur_type != '[' and cur_type != ']':
                continue
           
            cur_boxes = [(cur_x, cur_y)]

            # if type is [ or ] and we are moving up/down, not left/right
            #   we need to accordingly add left/right to move and to evalute next
            if cur_type == '[' and dx == 0:
                cur_boxes.append((cur_x+1, cur_y))
            elif cur_type == ']' and dx == 0:
                cur_boxes.append((cur_x-1, cur_y))

            # Save all boxes to later move
            pushing.extend(cur_boxes)

            # Calculate and save the next coordinates and type for each current box
            for x, y in cur_boxes:
                new_paths_coordinates.append((x+dx, y+dy))
                new_paths_type.append(map[y+dy][x+dx])

        paths_coordinates = new_paths_coordinates
        paths_type = new_paths_type

    # If wall found before open space, robot cant move:
    if '#' in paths_type:
        return robot_position
    
    # We have available space, move robot and all boxes in direction of move
    # Move boxes forward (In reverse order to ensure they dont overwrite each other)
    for x, y in reversed(pushing):
        map[y+dy][x+dx] = map[y][x]
        map[y][x] = '.'

    # Move robot forward
    map[rob_y][rob_x] = '.' # Set previous position of robot to empty
    map[rob_y+dy][rob_x+dx] = '@' # Set new position of robot
    
    return (rob_x+dx, rob_y+dy) 


test = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""


useTestInput = False
map, moves, robot_position = readInput(useTestInput, test)

directions = {
    '^': (0, -1),   # north
    '>': (1, 0),   # east
    'v': (0, 1),  # south
    '<': (-1, 0)   # west
}

print(task1(copy.deepcopy(map), moves, directions, robot_position))

print(task2(map, moves, directions, robot_position))