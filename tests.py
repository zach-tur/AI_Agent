from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file


def test():
    result = get_files_info("directory", ".")
    print(result)


if __name__ == "__main__":
    test()
