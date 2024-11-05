import os
import sys
import re
import ast


# Existing checks
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


def check_extra_spaces_after_keyword(line, line_number):
    match = re.match(r"^\s*(class|def)\s{2,}\w", line)
    if match:
        return f"Line {line_number}: S007 Too many spaces after '{match.group(1)}'"
    return None


def check_camel_case_class_name(line, line_number):
    if line.strip().startswith("class "):
        class_name = line.split()[1].split("(")[0].rstrip(":")
        if not re.match(r"^[A-Z][a-zA-Z0-9]*$", class_name):
            return f"Line {line_number}: S008 Class name '{class_name}' should use CamelCase"
    return None


def check_snake_case_function_name(line, line_number):
    if line.strip().startswith("def "):
        function_name = line.split()[1].split("(")[0]
        if not re.match(r"^[a-z_][a-z0-9_]*$", function_name):
            return f"Line {line_number}: S009 Function name '{function_name}' should use snake_case"
    return None


def check_snake_case_argument_names(node, file_path):
    errors = []
    for arg in node.args.args:
        if not re.match(r"^[a-z_][a-z0-9_]*$", arg.arg):
            errors.append(f"{file_path}: Line {arg.lineno}: S010 Argument name '{arg.arg}' should be snake_case")
    return errors


def check_snake_case_variable_names(node, file_path):
    errors = []
    for child in ast.walk(node):
        if isinstance(child, ast.Assign):
            for target in child.targets:
                if isinstance(target, ast.Name) and not re.match(r"^[a-z_][a-z0-9_]*$", target.id):
                    errors.append(
                        f"{file_path}: Line {target.lineno}: S011 Variable '{target.id}' in function should be snake_case")
    return errors


def check_mutable_default_arguments(node, file_path):
    errors = []
    mutable_types = (ast.List, ast.Dict, ast.Set)
    for arg, default in zip(node.args.args, node.args.defaults):
        if isinstance(default, mutable_types):
            errors.append(f"{file_path}: Line {default.lineno}: S012 Default argument value is mutable")
    return errors


def analyze_ast(file_path):
    errors = []
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            errors.extend(check_snake_case_argument_names(node, file_path))
            errors.extend(check_snake_case_variable_names(node, file_path))
            errors.extend(check_mutable_default_arguments(node, file_path))

    return errors


def analyze_file(file_path):
    file_path = os.path.normpath(file_path)
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
            check_blank_lines(lines, line_number),
            check_extra_spaces_after_keyword(line, line_number),
            check_camel_case_class_name(line, line_number),
            check_snake_case_function_name(line, line_number)
        ]
        errors.extend([f"{file_path}: {check}" for check in checks if check])

    errors.extend(analyze_ast(file_path))

    return errors


def analyze_directory(directory_path):
    all_errors = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                all_errors.extend(analyze_file(file_path))
    return all_errors


def main():
    if len(sys.argv) < 2:
        print("Please provide a directory or file path.")
        sys.exit(1)

    path = sys.argv[1]
    all_errors = []

    if os.path.isfile(path) and path.endswith('.py'):
        all_errors.extend(analyze_file(path))
    elif os.path.isdir(path):
        all_errors.extend(analyze_directory(path))
    else:
        print("Provided path is neither a .py file nor a directory.")
        sys.exit(1)

    def sort_key(error):
        path_part, rest = error.split(": ", 1)
        line_number = int(rest.split()[1][:-1])
        error_code = rest.split()[2]
        return (path_part, line_number, error_code)

    all_errors.sort(key=sort_key)

    for error in all_errors:
        print(error)


if __name__ == "__main__":
    main()
