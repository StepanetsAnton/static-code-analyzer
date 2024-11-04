def check_line_length(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line_number, line in enumerate(lines, start=1):
        if len(line) > 79:
            print(f"Line {line_number}: S001 Too long")

if __name__ == "__main__":
    file_path = input().strip()
    check_line_length(file_path)
