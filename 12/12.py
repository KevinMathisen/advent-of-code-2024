import queue

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

    return lines, bounds



# Task 1
def task1(map, bounds, directions):
    # Want to find each region in the map, 
    #   where a region contiguous plots with the same character, i.e. plant type
    # For each region, we want to count the total amount of area and perimeter

    # Generate the regions
    region_plots = {}
    biggest_region_id = 0

    # Iterate through each plot
    for y in range(len(map)):
        for x in range(len(map[y])):
            # Check if the plot already is in a region
            plot_part_of_region = False
            for region_id, plots in region_plots.items():
                if (x, y) in plots:
                    plot_part_of_region = True
                    break
            if plot_part_of_region:
                continue

            # Generate a region and save its plots
            region_plots[biggest_region_id] = get_region_plots(x, y, map, bounds, directions)

            biggest_region_id += 1

    # Create a map where each plot is the region id it belongs to
    region_map = [[-1 for x in range(len(map[y]))] for y in range(len(map))]
    for region_id, plots in region_plots.items():
        for x, y in plots:
            region_map[y][x] = region_id

    # Task 1
    # Iterate through each plot in the regions map
    regions_size = {}
    for y in range(len(region_map)):
        for x in range(len(region_map[y])):
            region_id = region_map[y][x]
            regions_size.setdefault(region_id, [0, 0])

            # Update the region area with 1, and the perimeter with the amount of perimeters for the plot
            regions_size[region_id][0] += 1
            regions_size[region_id][1] += get_perimeter_plot(x, y, region_map, bounds, directions)
    
    # Calculate the sum of the area multiplied with the permimeter for all of the regions
    task1 = sum([ area*perimeter for area, perimeter in regions_size.values() ])

    # Task 2
    # Want to find amount of sides and area for each region
    # Therfore start by finding all borders and the area for all regions
    regions_borders = {} # each region should have [<area>, <sides>, <borders>]
    for y in range(len(region_map)):
        for x in range(len(region_map[y])):
            # Update area and borders for the region each plot belongs to
            region_id = region_map[y][x]
            regions_borders.setdefault(region_id, [0, 0, set()]) # area, sides, borders
            regions_borders[region_id][0] += 1
            # Borders are saved as (x, y, direction)
            regions_borders[region_id][2].update(get_borders_plot(x, y, region_map, bounds, directions))

    # Find sides of regions by using their borders
    for region_id, (_, _, borders) in regions_borders.items():
        unique_sides = set() # Each unique side is a set of all borders it contains
        for border in borders:
            # Check if border already in a side
            border_in_side = False
            for unique_side in unique_sides:
                if border in unique_side:
                    border_in_side = True
                    break
            if border_in_side:
                continue

            # Border not in a side
            # Create new side with the border and any other borders beloning to it
            unique_sides.add(frozenset(get_side_for_border(border, borders)))

        # Save amount of sides for each region
        regions_borders[region_id][1] = len(unique_sides)

    #
    task2 = sum([ area*sides for area, sides, _ in regions_borders.values() ])

    return task1, task2

def get_region_plots(x, y, map, bounds, directions):
    plots_in_region = set()
    plots_to_inspect = queue.Queue()

    # Initialize plot in region to the first plot we look at
    plots_in_region.add((x, y))
    plots_to_inspect.put((x, y))

    # Visit plots are long as we find more plots in the region
    while not plots_to_inspect.empty():
        plotx, ploty = plots_to_inspect.get()
        
        # check if any of neighbours are also in the region 
        # not if out of bounds, if different character, or if already added
        for dx, dy in directions:
            next_x, next_y = plotx + dx, ploty + dy
            if (next_x, next_y) in plots_in_region:
                continue
            if next_x < bounds["min_x"] or next_x > bounds["max_x"] or next_y < bounds["min_y"] or next_y > bounds["max_y"]:
                continue
            if map[ploty][plotx] != map[next_y][next_x]:
                continue
            # Neighbour is in same region:
            plots_in_region.add((next_x, next_y))
            plots_to_inspect.put((next_x, next_y))

    return plots_in_region

def get_perimeter_plot(x, y, map, bounds, directions):
    # Check each direction
    # if out of bounds, or not same region, this adds one to perimeter
    perimeter_count = 0
    for dx, dy in directions:
        next_x = x+dx
        next_y = y+dy
        if next_x < bounds["min_x"] or next_x > bounds["max_x"] or next_y < bounds["min_y"] or next_y > bounds["max_y"]:
            perimeter_count+=1
        elif map[y][x] != map[next_y][next_x]:
            perimeter_count+=1

    return perimeter_count

# Task 2
def task2(map, bounds, directions):
    pass # See task 1

def get_borders_plot(x, y, map, bounds, directions):
    borders = set() # Each border is (x, y, direction)

    i = 0 # Use i to indicate direction of border, 0 = N, 1 = E, 2 = S, 3 = W

    # Check each direction
    # if out of bounds, or not same region, this adds one border
    for dx, dy in directions:
        next_x = x+dx
        next_y = y+dy
        if next_x < bounds["min_x"] or next_x > bounds["max_x"] or next_y < bounds["min_y"] or next_y > bounds["max_y"]:
            borders.add((x, y, i))
        elif map[y][x] != map[next_y][next_x]:
            borders.add((x, y, i))
        i+=1

    return borders

def get_side_for_border(border, borders):
    # Each side is a line of unabstructed plots with borders at same side
    # Starting from one border we can then check if any other borders are in the same side
    #  by checking the direction of the border
    
    borders_in_side = set()
    borders_to_check = queue.Queue()

    # Initialize side with the border we start at
    borders_in_side.add(border)
    borders_to_check.put(border)

    # north and south -> need to move along x axis, y axis for east/west
    map_directions_to_delta_xy = [(1, 0), (0, 1), (1, 0), (0, 1)]

    # As long as there are more borders to evaluate for the side
    while not borders_to_check.empty():
        
        # Get border, and directon to check for more borders based on the direction of the border
        border_to_check = borders_to_check.get()
        dx, dy = map_directions_to_delta_xy[border_to_check[2]]

        # Try to add in both directions, trying to find any border which will fit the side
        for border in borders:
            # check if the border fits East/south
            if (border[0], border[1]) == (border_to_check[0]+dx, border_to_check[1]+dy):
                if border[2] == border_to_check[2] and border not in borders_in_side:
                    borders_in_side.add(border)
                    borders_to_check.put(border)
            # check if the border fits North/west
            elif (border[0], border[1]) == (border_to_check[0]-dx, border_to_check[1]-dy):
                if border[2] == border_to_check[2] and border not in borders_in_side:
                    borders_in_side.add(border)
                    borders_to_check.put(border)
       
    return borders_in_side

test = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
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