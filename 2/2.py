def readInput(useTestInput, test):
    if not useTestInput:
        with open("input.txt") as file:
            content = file.read()
    else:
        content = test

    reports_string = [report.split(" ") for report in list(content.strip().split("\n"))]
    reports = [[int(level) for level in report] for report in reports_string]

    return reports



# Task 1
def task1(reports):
    amount_of_safe_reports = 0
    for report in reports:
        if is_report_safe(report):
            amount_of_safe_reports+=1

    return amount_of_safe_reports

def is_report_safe(report):
    report_safe = True
    report_increasing = (report[0]-report[1] < 0)

    # Get value of each step. If oposite signature (negative/positive than first) or bigger than 3 or 0, not safe
    for i in range(1, len(report)):
        step = report[i] - report[i-1]
        if step == 0 or abs(step) > 3 or (step < 0 and report_increasing) or (step > 0 and not report_increasing):
            report_safe = False
            break

    return report_safe

# Task 2
def task2(reports):
    amount_of_safe_reports = 0
    for report in reports:
        if is_report_safe(report):
            amount_of_safe_reports+=1
        else:
            for i in range(len(report)):
                if is_report_safe(report[:i]+report[i+1:]):
                    amount_of_safe_reports+=1
                    break

    return amount_of_safe_reports

test = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

useTestInput = False
input = readInput(useTestInput, test)

print(task1(input))

print(task2(input))