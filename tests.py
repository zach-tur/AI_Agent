from functions.get_files_info import get_files_info


def test():
    result = get_files_info("calculator", ".")
    print(f"Result for current directory:")
    print(result)

    result = get_files_info("calculator", "pkg")
    print(f"Result for 'pkg' directory:")
    print(result)

    result = get_files_info("calculator", "/bin")
    print(f"Result for '/bin' directory:")
    print(result)

    result = get_files_info("calculator", "../")
    print(f"Result for '../' directory:")
    print(result)


if __name__ == "__main__":
    test()
