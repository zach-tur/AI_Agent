import os
from functions.config import MAX_CHARS

from google import genai
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read content from. If the file size exceeds MAX_CHARS, result is truncated.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(full_path)
    abs_working = os.path.abspath(working_directory)
    if not abs_path.startswith(abs_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(full_path) > MAX_CHARS:
                file_content_string += (
                    '[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return file_content_string

    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
