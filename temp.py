def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    lines = list(content.strip().split("\n"))

    return lines



# Task 1
def task1(input):
    pass


# Task 2
def task2(input):
    
    pass

test = """
"""

useTestInput = True
input = readInput(useTestInput, test)

print(task1(input))

print(task2(input))