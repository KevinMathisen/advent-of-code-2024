def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    lines = list(content.strip().split("\n"))

    equations = []
    for line in lines:
        test_value, equation = line.split(": ")
        equation = [int(test_value), [int(number) for number in equation.split(" ")]]
        equations.append(equation)

    return equations



# Task 1
def task1(input):
    # Have to find which equations can produce 
    # their test value with a combination of operators (+ and *)

    # Could then create states of possible values based on previous operations, 
    # and create two new for each step
    # when reached final step we can check if the test value is in any of the possible values
    #  if so the equation can work

    sum_test_values = 0

    for equation in input:
        possible_values = set()
        for number in equation[1]:
            # Simply add first number as only possible one
            if len(possible_values) == 0:
                possible_values.add(number)
                continue

            new_possible_values = set()
            # Calculate all new possible values based on number
            for value in possible_values:
                new_possible_values.add(value+number)
                new_possible_values.add(value*number)
                # This is task 2:
                new_possible_values.add(int(str(value)+str(number)))
            
            # Then update set 
            possible_values = new_possible_values

        # Check if test value is possible, if so add its test value
        if equation[0] in possible_values:
            sum_test_values += equation[0]

    return sum_test_values

# Task 2
def task2(input):
    # Solved.
    # See line 46
    pass

test = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

useTestInput = False
input = readInput(useTestInput, test)

print(task1(input))

print(task2(input))