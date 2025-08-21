from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content


# def test_get_files_info():
#    result = get_files_info("calculator", ".")
#    print(f"Result for current directory:")
#    print(result)
#
#    result = get_files_info("calculator", "pkg")
#    print(f"Result for 'pkg' directory:")
#    print(result)
#
#    result = get_files_info("calculator", "/bin")
#    print(f"Result for '/bin' directory:")
#    print(result)
#
#    result = get_files_info("calculator", "../")
#    print(f"Result for '../' directory:")
#    print(result)


# def test_get_file_content():
#    result = get_file_content("calculator", "lorem.txt")
#    print(result)


def test_get_file_content():
    result = get_file_content("calculator", "main.py")
    print(result)

    result = get_file_content("calculator", "pkg/calculator.py")
    print(result)

    result = get_file_content("calculator", "bin/cat")
    print(result)

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result)


if __name__ == "__main__":
    #    test_get_files_info()
    test_get_file_content()
