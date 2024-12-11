def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    return [number for number in content.strip().split(" ")]


# Task 1
def task1(stones):
    times_to_blink = 25
    for i in range(times_to_blink):
        new_stones = []
        # Update each stone based on which rule apply:
        #   0 -> 1
        #   even number of digits -> split in two
        #   else multiply by 2048
        for stone in stones:
            if int(stone) == 0:
                new_stones.append('1')
            elif len(stone) % 2 == 0:
                midpoint = int(len(stone)/2)
                new_stones.append(str(int(stone[:midpoint])))
                new_stones.append(str(int(stone[midpoint:])))
            else:
                new_stones.append(str(2024*int(stone)))

        # Save new stones 
        stones = new_stones
    
    return len(stones)


# Task 2
def task2(stones):
    # Instead of storing all distinct stones, and doing operations on each,
    #  we can store the distinct stone types (as there will be a lot of stones with the same number)
    # Can then count how many there are of each type, and modify all at a time

    # Initialize all stones with count of 1
    stones_count = {}
    for stone in stones:
        stones_count[stone] = 1

    times_to_blink = 75
    for i in range(times_to_blink):
        new_stone_counts = {}
        # For each type of stone, update it based on which rule applies
        #   0 -> 1
        #   even number of digits -> split in two
        #   else multiply by 2048
        for stone, count in stones_count.items():
            if int(stone) == 0:
                new_stone_counts['1'] = new_stone_counts.setdefault('1', 0) + count
            elif len(stone) % 2 == 0:
                midpoint = int(len(stone)/2)
                stone1, stone2 = str(int(stone[:midpoint])), str(int(stone[midpoint:]))
                new_stone_counts[stone1] = new_stone_counts.setdefault(stone1, 0) + count
                new_stone_counts[stone2] = new_stone_counts.setdefault(stone2, 0) + count
            else:
                new_stone = str(2024*int(stone))
                new_stone_counts[new_stone] = new_stone_counts.setdefault(new_stone, 0) + count

        # Save new stones
        stones_count = new_stone_counts
    
    return sum([count for count in stones_count.values()])

test = """
125 17
"""

useTestInput = False
input = readInput(useTestInput, test)

print(task1(input))

print(task2(input))