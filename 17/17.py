import math

def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    registers_string, program_string = list(content.strip().split("\n\n"))

    registers = [int(line.split(": ")[1]) for line in registers_string.split("\n")]
    program = [int(number) for number in program_string.split(": ")[1].split(",")]

    return registers, program



# Task 1
def task1(registers, program):
    # Read opcode's from the instruction pointer (corresponding to instructions) until the program halts
    #   instruction pointer is increased by two after each read value, except for jump
    #
    # Also maintain registries A, B, and C
    # 
    # Operands are values used by instructions, where each instruction is read as <opcode> <operand>
    #   Operand can be literal, i.e. they are their value
    #   Can also be combo, where 0-3 is literal, 4 = register A, 5 = B, 6 = C, and 7 is not used in valid program
    #  
    # Opcode to inctruction mapping:
    #   - 0 adv: divide A by 2^combo -> A
    #   - 1 bxl: bitwise XOR of B and literal operand -> B
    #   - 2 bst: combo mod 8 -> B
    #   - 3 jnz: if A!=0 -> jump to literal operand, then do not increase instruction pointer by 2
    #   - 4 bxc: bitwise XOR of B and C -> B
    #   - 5 out: compo mod 8 -> output
    #   - 6 bdv: divide A by 2^combo -> B
    #   - 7 cdv: divide A by 2^combo -> C
    #
    # Want to run program, saving values to output, then return string of these joines by ','
    output = []

    instruction_pointer = 0
    while instruction_pointer < len(program):
        instruction_pointer, output_value = perform_instruction(registers, program, instruction_pointer)
        if output_value != -1:
            output.append(output_value)

    return ','.join(map(str, output))

def perform_instruction(registers, program, instruction_pointer):
    opcode, operand = program[instruction_pointer], program[instruction_pointer+1]
    output_value = -1

    if opcode == 0:
        registers[0] = int(registers[0] / math.pow(2, get_literal_value_from_combo(operand, registers)))
    elif opcode == 1:
        registers[1] ^= operand
    elif opcode == 2:
        registers[1] = get_literal_value_from_combo(operand, registers) % 8
    elif opcode == 3:
        if registers[0] != 0 and operand != instruction_pointer:
            return operand, output_value
    elif opcode == 4:
        registers[1] = registers[1] ^ registers[2]
    elif opcode == 5:
        output_value = get_literal_value_from_combo(operand, registers) % 8
    elif opcode == 6 or opcode == 7:
        registers[opcode-5] = int(registers[0] / math.pow(2, get_literal_value_from_combo(operand, registers)))

    return instruction_pointer+2, output_value

def get_literal_value_from_combo(combo, registers):
    if combo <= 3:
        return combo
    return registers[combo-4]

# Task 2
def task2(registers, program):
    # Want to find the value of A which makes the output equal to the program
    # Know that the program ends when A is 0. 
    # Can therefore use the last instruction before the program ends
    #       to calculate the possible values of A ending the program
    # Can check which of these values generate a new output where 
    #       the first value in the output matches the last value in the program. 
    # When we get A values which match, we again perform the operation on these, 
    #       calculating the possible values of A on top of this which are also possible.
    # Can then again on these new values check if their output matches the program. 
    #       each new iteration of A increases the output by one. 
    # Can do this repeadedly until we get enough output values which match the program. 
    #       We then choose the lowest value of these A values.

    # Temporary solution, takes to long:
    
    # Want to try values of register A until the output of the program is equal to the program
    init_A = -1
    while True: # As long as the output is not the same as the input
        init_A += 1
        invalid_A = False

        registers = [init_A, 0, 0]
        instruction_pointer = 0
        output_index = -1

        program_output = []

        while instruction_pointer < len(program):
            instruction_pointer, output_value = perform_instruction(registers, program, instruction_pointer)

            # If any output_value differs from program, we can go to next A value
            if output_value != -1:
                output_index += 1
                program_output.append(output_value)

                if output_value != program[output_index]:
                    invalid_A = True
                    break

        if not invalid_A and program_output == program:
            return init_A
        
        if init_A % 1000000 == 0:
            print(f'Checked values of A up to {init_A}')

test1 = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""
test = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""

useTestInput = False
registers, program = readInput(useTestInput, test)

print(task1(registers, program))

print(task2(registers, program))