import os


def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(full_path)
    abs_working = os.path.abspath(working_directory)

    if not abs_path.startswith(abs_working):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(os.path.dirname(abs_path)):
        try:
            os.makedirs(os.path.dirname(abs_path))
        except Exception as e:
            return f"Error: creating directory: {e}"

    if os.path.exists(abs_path) and os.path.isdir(abs_path):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        with open(abs_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error writing to file: {e}"
