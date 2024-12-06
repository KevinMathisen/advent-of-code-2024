def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    lines = list(content.strip().split("\n"))

    list1 = []
    list2 = []
    for pair in lines: 
        numbers = [int(number) for number in pair.split()]
        list1.append(numbers[0])
        list2.append(numbers[1])

    return (list1, list2)



# Task 1
def task1(list1, list2):
    list1.sort()
    list2.sort()

    # Assume same length
    distances = [abs(list1[i]-list2[i]) for i in range(len(list1))]
    return sum(distances)


# Task 2
def task2(list1, list2):
    return sum([num1 * len([num2 for num2 in list2 if num2 == num1]) for num1 in list1])


test = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

useTestInput = False
(list1, list2) = readInput(useTestInput, test)

print(task1(list1, list2))
print(task2(list1, list2))