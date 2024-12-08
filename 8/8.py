from collections import defaultdict

def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    # want to have dictinary of different character
    # each one should have a set with coordinates of its towers

    lines = list(content.strip().split("\n"))

    antennas = defaultdict(set)
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == '.':
                continue
            antennas[lines[y][x]].add((x, y))

    bounds = {
        "min_y": 0,
        "max_y": len(lines)-1,
        "min_x": 0,
        "max_x": len(lines[0])-1
    }

    return antennas, bounds

def print_map(antennas, bounds, antinodes):
    for y in range(bounds["min_y"], bounds["max_y"] + 1):
        line = ""
        for x in range(bounds["min_x"], bounds["max_x"] + 1):
            found = False
            for char, coords in antennas.items():
                if (x, y) in coords:
                    line += char  # Draw the character corresponding to the antenna
                    found = True
                    break
            if not found:
                if (x, y) in antinodes:
                    line += "#"  # Antinode
                else:
                    line += "."  # Empty space
        print(line)
    print("\n" + "-" * (bounds["max_x"] - bounds["min_x"] + 1) + "\n")


# Task 1
def task1(antennas, bounds):
    # For each type of antenna, we have to find all locations of antinodes
    # So for each antenna, we have to iterate through all others, 
    # using their distance to find antinodes for this antenna

    # Add all antinodes found to set, then count amount at end

    antinodes = set()

    for antennas_type in antennas.values():
        # For each antenna
        for antenna in antennas_type:
            # compare it with all other antennas (except self)
            for antenna_to_compare in antennas_type:
                if antenna_to_compare == antenna:
                    continue

                # Calculate delta x and delta y between them
                dx = antenna_to_compare[0] - antenna[0]
                dy = antenna_to_compare[1] - antenna[1]

                # Find coordinate of antinode
                antinode_x = antenna[0]-dx
                antinode_y = antenna[1]-dy

                # Check if within bounds, if so add to set
                if antinode_x >= bounds["min_x"] and antinode_x <= bounds["max_x"] and antinode_y >= bounds["min_y"] and antinode_y <= bounds["max_y"]:
                    antinodes.add((antinode_x, antinode_y))

    print_map(antennas, bounds, antinodes)

    return len(antinodes)


# Task 2
def task2(antennas, bounds):
    # For each type of antenna, we have to find all locations of antinodes
    # So for each antenna, we have to iterate through all others, 
    # using their distance to find antinodes for this antenna

    # Add all antinodes found to set, then count amount at end

    # Task 2 needs us to not only fins one antinode delta x/y from node
    # But find multiplyer of delta x/y antinodes until we go out of bounds

    antinodes = set()

    for antennas_type in antennas.values():
        # For each antenna
        for antenna in antennas_type:
            # compare it with all other antennas (except self)
            for antenna_to_compare in antennas_type:
                if antenna_to_compare == antenna:
                    continue

                # Calculate delta x and delta y between them
                dx = antenna_to_compare[0] - antenna[0]
                dy = antenna_to_compare[1] - antenna[1]

                # Find coordinate of antinode
                antinode_x = antenna[0]
                antinode_y = antenna[1]

                # While antinodes within bounds, save them
                while antinode_x >= bounds["min_x"] and antinode_x <= bounds["max_x"] and antinode_y >= bounds["min_y"] and antinode_y <= bounds["max_y"]:
                    antinodes.add((antinode_x, antinode_y))
                    antinode_x -= dx
                    antinode_y -= dy

    print_map(antennas, bounds, antinodes)

    return len(antinodes)

test = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

useTestInput = False
antennas, bounds = readInput(useTestInput, test)

print(task1(antennas, bounds))

print(task2(antennas, bounds))