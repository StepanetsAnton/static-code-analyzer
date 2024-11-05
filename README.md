# Static Code Analyzer

A Python static code analyzer to enforce code style and PEP8 standards. This project analyzes Python code files and directories, checking for various style violations and issues in code structure. It uses Python's `ast` (Abstract Syntax Tree) module for some checks to ensure that variables, function arguments, and function definitions follow best practices.

## Features

This analyzer checks for:
- Line length and indentation issues
- Unnecessary semicolons and inline comment spacing
- "TODO" comments in the code
- CamelCase and snake_case naming conventions for classes and functions
- Mutable default argument values in function definitions
- Argument and variable naming styles within functions

## Installation

To get started, clone this repository to your local machine and navigate to the project directory:

```bash
git clone https://github.com/your-username/static-code-analyzer.git
cd static-code-analyzer
```

## Usage
Run the static code analyzer on a file or directory by passing the path as a command-line argument:

```bash
python code_analyzer.py <path-to-file-or-directory>
```

For example:
```bash
python code_analyzer.py example.py
python code_analyzer.py path/to/project
```

The output will display the file path, line number, error code, and a description of each issue found.

## Example Output
```bash
example.py: Line 5: S001 Too long
example.py: Line 10: S002 Indentation is not a multiple of four
example.py: Line 12: S007 Too many spaces after 'class'
example.py: Line 20: S010 Argument name 'ArgName' should be snake_case
example.py: Line 25: S012 Default argument value is mutable
```

## Checks Performed
Here are the checks the analyzer performs, along with their codes:

Code	Description
S001	Line exceeds 79 characters.
S002	Indentation is not a multiple of four.
S003	Unnecessary semicolon at the end of a statement.
S004	At least two spaces required before inline comments.
S005	"TODO" found in comments.
S006	More than two blank lines before this line.
S007	Too many spaces after 'class' or 'def' keyword.
S008	Class name should use CamelCase.
S009	Function name should use snake_case.
S010	Argument name should be in snake_case.
S011	Variable name within a function should be in snake_case.
S012	Default argument value is mutable.
## Code Structure
The analyzer consists of:

Regular expression-based checks for line length, indentation, semicolons, comments, etc.
AST-based checks to analyze function arguments, variable names, and default argument values.
## Dependencies
This project uses only built-in Python libraries, specifically:

re: For regular expressions.
ast: For analyzing function structures and argument definitions.
## Contributing
If you’d like to contribute:

Fork this repository.
Create a new branch for your feature (git checkout -b feature-name).
Commit your changes (git commit -m 'Add feature').
Push to the branch (git push origin feature-name).
Open a Pull Request.
