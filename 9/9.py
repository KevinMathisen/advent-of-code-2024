def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    content = content.strip()

    blocks = []
    file_positions = []
    free_space_positions = []
    file_id = 0
    position = 0
    # Convert input to list with numbers and -1 where empty
    # And to lists of the file locations and free space locations
    for i in range(len(content)):
        if i%2 == 0: # File:
            file_length = int(content[i])
            # Write amount of blocks with its ID
            for j in range(file_length):
                blocks.append(file_id)

            # Also write its id, position, and length
            file_positions.append((file_id, position, file_length))

            file_id+=1
            position+=file_length

        else: # Free space
            free_space_length = int(content[i])
            # Write amount of blocks it takes
            for j in range(int(free_space_length)):
                blocks.append(-1)

            # Write its position and length
            free_space_positions.append((position, free_space_length))

            position+=free_space_length

    return blocks, file_positions, free_space_positions

# Task 1
def task1(blocks):
    # Want to move block files into free space

    # Have two pointers, one for left and one for right. 
    # Left points to free space (-1), iterating from left to right
    # Right points to files (>-1), iterating from right to left
    # As long as these have not reached the same position, we can continue to move files

    # Find initial left and right positions
    left_pos = blocks.index(-1)
    right_pos = len(blocks) - 1
    while (blocks[right_pos]==-1):
        right_pos-=1

    # As long as there is more empty blocks to move files to
    while (left_pos < right_pos):
        # Move block with file in into block with free space
        blocks[left_pos] = blocks[right_pos]
        blocks[right_pos] = -1

        # iterate positions, moving left to first free space, and right to first file (in reverse)
        left_pos = blocks.index(-1, left_pos)
        while (blocks[right_pos]==-1):
            right_pos-=1

    # Calculate checksum for each block as file_id*block_pos
    return sum([i*blocks[i] for i in range(len(blocks)) if blocks[i] != -1])

# Task 2
def task2(file_positions, free_space_positions):
    # Still want to move files into free space, however now we move whole file at a time, not in blocks
    
    # Try to move each file (in reverse order, starting at end of blocks)
    for i in range(len(file_positions)-1, -1, -1):
        (file_id, file_pos, file_len) = file_positions[i]
        
        # Check all free spaces if they have enough space
        for j in range(len(free_space_positions)):
            (free_space_pos, free_space_len) = free_space_positions[j]       
            
            # If we can move the file, i.e. if it fits and free space is before it
            if file_len <= free_space_len and file_pos > free_space_pos:
                # Update file by moving it
                file_positions[i] = (file_id, free_space_pos, file_len)

                # Update free space by removing space used by file
                free_space_positions[j] = (free_space_pos+file_len, free_space_len-file_len)
                
                # Break out of loop, as does not need to move file again
                break

    # Calculate checksom by getting sum of the ids of files in blocks times block position
    return sum([file_id * (file_pos+i) for (file_id, file_pos, file_len) in file_positions for i in range(file_len)])

test = """
2333133121414131402
"""

useTestInput = False
blocks, file_positions, free_space_positions = readInput(useTestInput, test)

print(task1(blocks))

print(task2(file_positions, free_space_positions))