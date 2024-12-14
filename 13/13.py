import re
import numpy as np
import math

def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    machines_string = list(content.strip().split("\n\n"))

    button_pattern = r".*X\+(\d+), Y\+(\d+)"
    prize_pattern = r".*X=(\d+), Y=(\d+)"

    machines = []

    for machine_string in machines_string:
        button_a_string, button_b_string, prize_string = machine_string.split("\n")
        button_a_match = re.search(button_pattern, button_a_string)
        button_b_match = re.search(button_pattern, button_b_string)
        prize_match = re.search(prize_pattern, prize_string)

        machine = {
            'a': (int(button_a_match.group(1)), int(button_a_match.group(2))),
            'b': (int(button_b_match.group(1)), int(button_b_match.group(2))),
            'prize': (int(prize_match.group(1)), int(prize_match.group(2)))
        }

        machines.append(machine)
    
    return machines

# Task 1
def task1(machines):
    # Find minimum amount of tokens needed to reach goal 
    # I.e. combination of A and B presses leading to goal

    # i -> times pressed A, j -> times pressed B
    # i * a_x + j * b_x = prize_x
    # i * a_y + j * b_y = prize_y
    
    # This is a system of linear equations, 
    #  where we have two linear equations, one for x coordinates and one for y coordinates
    #  and the variables are the amount of times we want to press the buttons
    # Can solve this by using matrices in the form Ax=B (see https://en.wikipedia.org/wiki/System_of_linear_equations#Matrix_solution)
    #   where we can find x (times a and b needs to be pressed) by A^-1 b
    #   or by simply using np.linalg.solve()

    # Find the tokens needed to reach the prize for all machines
    sum_tokens = 0
    for machine in machines:
        a_x, a_y = machine['a'][0], machine['b'][0]
        b_x, b_y = machine['a'][1], machine['b'][1]
        prize_x, prize_y = machine['prize'][0], machine['prize'][1]
        
        # Create coefficient matrix of the step sizes for the buttons
        A = np.array([[a_x, a_y],
                    [b_x, b_y]])
        
        # Create constants matrix for the x and y values we want to reach (the prize)
        B = np.array([prize_x, prize_y])

        # Check the determinant to know if there exists a unique way to press the buttons to reach the prize
        if np.linalg.det(A) != 0: 
            # There is a unique solution 
            a_presses, b_presses = np.linalg.solve(A, B)
            
            # If the solution we found contains whole numbers, i.e. a real solution for the buttons we can click, we add the token count
            if is_close_to_integer(a_presses) and is_close_to_integer(b_presses):
                sum_tokens += int(round(a_presses))*3 + int(round(b_presses))

    return sum_tokens

# Task 2
def task2(machines):
    # Same solution to task1, only adding 10000000000000 to the prize coordinates
    
    # Find the tokens needed to reach the prize for all machines
    sum_tokens = 0
    for machine in machines:
        a_x, a_y = machine['a'][0], machine['b'][0]
        b_x, b_y = machine['a'][1], machine['b'][1]
        prize_x, prize_y = machine['prize'][0]+10000000000000, machine['prize'][1]+10000000000000
        
        # Create coefficient matrix of the step sizes for the buttons
        A = np.array([[a_x, a_y],
                    [b_x, b_y]])
        
        # Create constants matrix for the x and y values we want to reach (the prize)
        B = np.array([prize_x, prize_y])

        # Check the determinant to know if there exists a unique way to press the buttons to reach the prize
        if np.linalg.det(A) != 0: 
            # There is a unique solution 
            a_presses, b_presses = np.linalg.solve(A, B)
            
            # If the solution we found contains whole numbers, i.e. a real solution for the buttons we can click, we add the token count
            if is_close_to_integer(a_presses) and is_close_to_integer(b_presses):
                sum_tokens += int(round(a_presses))*3 + int(round(b_presses))

    return sum_tokens

def is_close_to_integer(value, tolerance=1e-4):
    return abs(value - round(value)) < tolerance

test = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

useTestInput = False
input = readInput(useTestInput, test)

print(task1(input))

print(task2(input))