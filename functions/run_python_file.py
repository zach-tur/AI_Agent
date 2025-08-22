import os
import subprocess
from sys import stderr, stdout
from threading import ExceptHookArgs

from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified file in the specified directory, with provided args. constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file name to be run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="The arguements provided to the file to be run.",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(full_path)
    abs_working = os.path.abspath(working_directory)
    if not abs_path.startswith(abs_working):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" not found.'

    if not abs_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ["python", file_path, *args],
            capture_output=True,
            cwd=abs_working,
            timeout=30,
        )

        if completed_process.returncode != 0:
            return f"Process exited with code {completed_process.returncode}"
        if completed_process.stdout == None:
            return "No output produced."

        if not completed_process.stdout and not completed_process.stderr:
            return f"No output produced."

        return f"STDOUT:\n{completed_process.stdout}\nSTDERR:\n{completed_process.stderr}\n"

    except Exception as e:
        return f"Error: executing Python file: {e}"
