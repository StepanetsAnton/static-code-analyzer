import re

def check_line_length(line, line_number):
    if len(line) > 79:
        return f"Line {line_number}: S001 Too long"
    return None

def check_indentation(line, line_number):
    leading_spaces = len(line) - len(line.lstrip(' '))
    if leading_spaces % 4 != 0:
        return f"Line {line_number}: S002 Indentation is not a multiple of four"
    return None

def check_unnecessary_semicolon(line, line_number):
    code_part = line.split('#')[0]
    in_string = False
    for i, char in enumerate(code_part):
        if char in ("'", '"'):
            if i == 0 or code_part[i - 1] != '\\':
                in_string = not in_string
        elif char == ';' and not in_string:
            return f"Line {line_number}: S003 Unnecessary semicolon"
    return None


def check_inline_comment_spacing(line, line_number):
    if '#' in line:
        code_part, comment_part = line.split('#', 1)

        if code_part and not code_part.endswith('  ') and code_part.strip():
            return f"Line {line_number}: S004 At least two spaces required before inline comments"
    return None


def check_todo_comment(line, line_number):
    if '#' in line and 'todo' in line.split('#', 1)[1].lower():
        return f"Line {line_number}: S005 TODO found"
    return None

def check_blank_lines(lines, line_number):
    if line_number >= 3:
        blank_count = 0
        for i in range(line_number - 2, -1, -1):
            if lines[i].strip() == "":
                blank_count += 1
            else:
                break
        if blank_count > 2:
            return f"Line {line_number}: S006 More than two blank lines used before this line"
    return None

def analyze_code(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    errors = []

    for line_number, line in enumerate(lines, start=1):
        checks = [
            check_line_length(line, line_number),
            check_indentation(line, line_number),
            check_unnecessary_semicolon(line, line_number),
            check_inline_comment_spacing(line, line_number),
            check_todo_comment(line, line_number),
            check_blank_lines(lines, line_number)
        ]
        errors.extend([check for check in checks if check])

    errors.sort(key=lambda error: (int(error.split()[1][:-1]), error.split()[2]))

    for error in errors:
        print(error)


if __name__ == "__main__":
    file_path = input().strip()
    analyze_code(file_path)
