def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    rules_content, pages_content = list(content.strip().split("\n\n"))

    rules = []
    for rule_string in rules_content.split("\n"):
        rules.append([int(page_num) for page_num in rule_string.split("|")])
    
    manuals = []
    for safety_manual_string in pages_content.split("\n"):
        manuals.append([int(page_num) for page_num in safety_manual_string.split(",")])

    return rules, manuals



# Task 1
def task1(rules, manuals):

    sum_middle_pages = 0

    for manual in manuals:
        # Check if manual is in right order
        # Have to check if each rule is followed
        # aka try to find a rule which has been broken
        # Can therefore for each number, get the rules where it is at the end. 
        # If any of the numbers after it matches the numbers which 
        # should be in front of it, it is not ordered correctly
        for i in range(len(manual)):
            manual_is_ordered = True
            pages_only_allowed_to_appear_before = [rule[0] for rule in rules if rule[1] == manual[i]]

            for j in range(i+1, len(manual)):
                if manual[j] in pages_only_allowed_to_appear_before:
                    manual_is_ordered = False
                    break

            if not manual_is_ordered:
                break

        if manual_is_ordered:
            sum_middle_pages += manual[int(len(manual)/2)]

    return sum_middle_pages


# Task 2
def task2(rules, manuals):
    sum_middle_pages = 0

    for manual in manuals:
        manual_is_ordered = True
        # Check if manual is in right order
        for i in range(len(manual)):
            # For each number, we need to check the numbers appearing before it.
            # First get the numbers with are NOT supposed to be before it

            # The first page we find which should appear before it, be need to switch the position with.
            # Does not need to consider any more number after this        
            for pos_num_appearing_before in range(i):
                pages_only_allowed_to_appear_after = [rule[1] for rule in rules if rule[0] == manual[i]]
                if manual[pos_num_appearing_before] in pages_only_allowed_to_appear_after:
                    current_num_value = manual[i]
                    manual[i] = manual[pos_num_appearing_before]
                    manual[pos_num_appearing_before] = current_num_value

                    manual_is_ordered = False
                    
        if not manual_is_ordered:
            sum_middle_pages += manual[int(len(manual)/2)]

    return sum_middle_pages

test = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

useTestInput = False
rules, manuals = readInput(useTestInput, test)

print(task1(rules, manuals))

print(task2(rules, manuals))