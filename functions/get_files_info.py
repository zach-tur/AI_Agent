import os
from google import genai
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    directory_path = os.path.join(working_directory, directory)
    abs_directory = os.path.abspath(directory_path)
    abs_working = os.path.abspath(working_directory)
    if not abs_directory.startswith(abs_working):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'
    try:
        lines = []
        for i in os.listdir(abs_directory):
            item = os.path.join(abs_directory, i)
            lines.append(
                f" - {i}: file_size={os.path.getsize(item)} bytes, is_dir={os.path.isdir(item)}"
            )
        return "\n".join(lines)

    except Exception as e:
        return f"Error: {e}"
