import re
import queue

def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    
    robots_strings = list(content.strip().split("\n"))

    robot_pattern = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"

    robots = []

    for robot_string in robots_strings:
        robot_match = re.match(robot_pattern, robot_string)

        robot = {
            'x': int(robot_match.group(1)),
            'y': int(robot_match.group(2)),
            'dx': int(robot_match.group(3)),
            'dy': int(robot_match.group(4)),
        }

        robots.append(robot)
    
    return robots

def print_map(robots, bounds):
    # create map
    map = [['.' for _ in range(bounds['max_x'])] for _ in range(bounds['max_y'])]
    for robot in robots:
        map[robot['y']][robot['x']] = 'R'

    # print map
    for row in map:
        print(''.join(row))

# Task 1
def task1(robots, bounds):
    # For each robot, we need to find which quadrant it ends up in after
    #  specified amount of seconds
    
    seconds = 100
    quadrant_counts = [0, 0, 0, 0]
    
    for robot in robots:
        final_x = (robot['x'] + robot['dx']*seconds) % bounds['max_x']
        final_y = (robot['y'] + robot['dy']*seconds) % bounds['max_y']

        # Count which quadrant the robot ends up in
        if final_y != bounds['max_y'] // 2 and final_x != bounds['max_x'] // 2:
            quadrant_index = (final_y >= bounds['max_y'] // 2) * 2 + (final_x >= bounds['max_x'] // 2)
            quadrant_counts[quadrant_index] += 1
    
    safety_factor = 1
    for quadrant_count in quadrant_counts:
        safety_factor*=quadrant_count
    
    return safety_factor


# Task 2
def task2(robots, bounds):
    # Need to find when the robots arrange into a christmas tree 
    # Dont know its structure, but can assume the robots are connected in the picture
    # Therefore want to find how long until a certain amount of robots are next to each other
    
    seconds_elapsed = 0
    treshhold_region_size = 200

    # As long as tree not found
    while True:
        seconds_elapsed+=1

        # Update position of all robots
        for i in range(len(robots)):
            robots[i]['x'] = (robots[i]['x'] + robots[i]['dx']) % bounds['max_x']
            robots[i]['y'] = (robots[i]['y'] + robots[i]['dy']) % bounds['max_y']
    
        # Create set of robot coordinates
        robot_coordinates = set()
        for robot in robots:
            robot_coordinates.add((robot['x'], robot['y']))
        robot_coordinates_list = list(robot_coordinates)

        # check if more than treshold amount of robots next to each other
        # Only check 1/3 of the robots, assuming some have to be in the Christmas tree
        for i in range(int(len(robot_coordinates_list) / 3)):
            robot = robot_coordinates_list[i]
            
            robot_count = get_robot_region(robot, robot_coordinates)

            # If a region found is larger than the treshhold, assume tree is found
            if robot_count > treshhold_region_size:
                print_map(robots, bounds)
                return seconds_elapsed

def get_robot_region(robot, robot_coordinates):
    # Find amount of robots connected to given robot

    robots_in_region = set()
    robots_queue = queue.Queue()

    robots_in_region.add(robot)
    robots_queue.put(robot)

    # Directions for neighboring positions
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # As long as there are more robots in region to consider
    while not robots_queue.empty():
        x, y = robots_queue.get()

        # Check if there are any neighbouring robots
        for dx, dy in directions:
            neighbor = (x+dx, y+dy)
            if neighbor not in robots_in_region and neighbor in robot_coordinates:
                robots_in_region.add(neighbor)
                robots_queue.put(neighbor)

    return len(robots_in_region)

test = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

bounds = {
    "min_y": 0,
    "max_y": 103,
    "min_x": 0,
    "max_x": 101
}

useTestInput = False
robots = readInput(useTestInput, test)

print(task1(robots, bounds))

print(task2(robots, bounds))