from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file


def test():
    result = run_python_file("calculator", "main.py")
    print(f"First result:\n{result}")

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(f"Second result:\n{result}")

    result = run_python_file("calculator", "tests.py")
    print(f"Third result:\n{result}")

    result = run_python_file("calculator", "../main.py")
    print(f"Fourth result:\n{result}")

    result = run_python_file("calculator", "nonexistent.py")
    print(f"Fifth result:\n{result}")


if __name__ == "__main__":
    test()
