def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    lines = list(content.strip().split("\n"))

    return lines



# Task 1
def task1():
    pass


# Task 2
def task2():
    
    pass

test = """
"""

useTestInput = True
input = readInput(useTestInput, test)

print(task1())

print(task2())