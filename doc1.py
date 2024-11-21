import os
import sys
import subprocess

# Function to check if a specific file exists in the repository
def check_file_exists(file_name):
    if not os.path.isfile(file_name): 
        print(f"Error: {file_name} is missing.")
        sys.exit(1)  # Exit with error code 1 if file is missing
    else:
        print(f"{file_name} exists.")

# Function to run tests using pytest
def run_tests():
    try:
        result = subprocess.run(['pytest', '--maxfail=1', '--disable-warnings', '-q'], 
                                capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Tests failed with the following output:\n{result.stdout}")
            sys.exit(result.returncode)  # Exit with the test return code
        else:
            print("Tests passed successfully.")
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)

# Function to check Python code for syntax errors using pyflakes
def check_syntax():
    try:
        result = subprocess.run(['pyflakes', '.'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Syntax errors found:\n{result.stdout}")
            sys.exit(result.returncode)  # Exit with the pyflakes error code
        else:
            print("No syntax errors detected.")
    except Exception as e:
        print(f"Error running pyflakes: {e}")
        sys.exit(1)

# Function to check for TODO comments in the code
def check_for_todo():
    todo_found = False
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    if 'TODO' in content:
                        print(f"TODO comment found in {file_path}")
                        todo_found = True
    if todo_found:
        sys.exit(1)  # Exit with error code if TODO comments are found
    else:
        print("No TODO comments found.")

if __name__ == "__main__":
    # Check if a README.md file exists
    check_file_exists('checks.yml')

    # Check if the requirements.txt file exists
    check_file_exists('main.yml')

    # Run syntax check
    check_syntax()

    # Run tests
    run_tests()

    # Check for TODO comments
    check_for_todo() 
