def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    lines = list(content.strip().split("\n"))

    return lines



# Task 1
def task1(lines):
    bounds = {
        "min_y": 0,
        "max_y": len(lines)-1,
        "min_x": 0,
        "max_x": len(lines[0])-1
    }
    

    directions = {
        "north": (0, 1),
        "north-east": (1, 1),
        "east": (1, 0),
        "south-east": (1, -1),
        "south": (0, -1),
        "south-west": (-1, -1),
        "west": (-1, 0),
        "north-west": (-1, 1)
    }

    xmas_count = 0
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == 'X':
                # Start search in places where we find X, trying to find in all directions
                for (dx, dy) in directions.values():
                    if search_direction(x, y, dx, dy, 0, lines, bounds):
                        xmas_count+=1
    
    return xmas_count

def search_direction(x, y, delta_x, delta_y, current_length, lines, bounds):
    expected_values = "XMAS"

    # If we have reached end of an expected value, we have a match
    if current_length >= len(expected_values)-1:
        return True
    
    next_x = x+delta_x
    next_y = y+delta_y

    # Check if next are out of bounds
    if next_x < bounds["min_x"] or next_x > bounds["max_x"] or next_y < bounds["min_y"] or next_y > bounds["max_y"]:
        return False

    # If next character matches expected, call again with new length
    if lines[next_y][next_x] == expected_values[current_length+1]:
        return search_direction(next_x, next_y, delta_x, delta_y, current_length+1, lines, bounds)

    # When no match found, return false
    return False

# Task 2
def task2(lines):
    bounds = {
        "min_y": 0,
        "max_y": len(lines)-1,
        "min_x": 0,
        "max_x": len(lines[0])-1
    }
    
    directions = {
        "north-east": (1, 1),
        "south-east": (1, -1),
        "south-west": (-1, -1),
        "north-west": (-1, 1)
    }

    x_mas_count = 0
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == 'A':
                # Start search in places where we find A, trying to find if crosses match
                # NE, SE, SW, NW
                characters = [get_character(x, y, direction, lines, bounds) for direction in directions.values()]
                
                if is_x_mas(characters):
                    x_mas_count+=1
    
    return x_mas_count

def get_character(x, y, delta_values, lines, bounds):
    delta_x, delta_y = delta_values

    # Coordinates to get character from
    next_x = x+delta_x
    next_y = y+delta_y

    # Check if out of bounds
    if next_x < bounds["min_x"] or next_x > bounds["max_x"] or next_y < bounds["min_y"] or next_y > bounds["max_y"]:
        return ''
    
    return lines[next_y][next_x]
    
def is_x_mas(characters):
    NE, SE, SW, NW = characters
    diagonal1 = False
    diagonal2 = False
    if NE == 'M' and SW == 'S' or NE == 'S' and SW == 'M':
        diagonal1 = True
    if NW == 'M' and SE == 'S' or NW == 'S' and SE == 'M':
        diagonal2 = True

    return diagonal1 and diagonal2


test = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

useTestInput = False
input = readInput(useTestInput, test)

print(task1(input))

print(task2(input))