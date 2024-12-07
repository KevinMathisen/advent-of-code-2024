import re

def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    # Assume no wrapping of commands between lines
    sections = list(content.strip().split("\n"))
    
    return sections


# Task 1
def task1(sections):
    pattern = re.compile(r'mul\((\d+),(\d+)\)')

    mul_result = 0
    for section in sections:
        matches = pattern.findall(section)
        for mul in matches:
            mul_result += int(mul[0]) * int(mul[1])

    return mul_result


# Task 2
def task2(sections):
    mul_pattern = re.compile(r'mul\((\d+),(\d+)\)')
    do_pattern = re.compile(r'do\(\)')
    dont_pattern = re.compile(r'don\'t\(\)')

    mul_result = 0
    merged_sections = ""
    for section in sections:
        merged_sections += section

    lines_with_do_start = do_pattern.split(merged_sections)

    for line_with_do in lines_with_do_start:
        section_to_execute = dont_pattern.split(line_with_do)[0]

        matches = mul_pattern.findall(section_to_execute)
        for mul in matches:
            mul_result += int(mul[0]) * int(mul[1])

    return mul_result

test = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""
test2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""

useTestInput = False
input = readInput(useTestInput, test)
input2 = readInput(useTestInput, test2)

print(task1(input))

print(task2(input2))