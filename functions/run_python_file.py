import os
from google.genai import types
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)
        
        # 'check=True' Validates target within working directory, and file existence before execution
        # 'text=True' Decode the output to strings, rather than bytes; this is done by setting text=True
        # 'capture_output=True' Capture the output of the command, so that it can be returned
        # 'timeout=30' Set a timeout of 30 seconds, to prevent the command from running indefinitely
        result = subprocess.run(command, text=True, capture_output=True, timeout=30, cwd=working_dir_abs)

        output_str = ""
        if result.returncode != 0:
            output_str += f'Process exited with code {result.returncode}'
        elif not (result.stdout or result.stderr):
            output_str += "No output produced"
        else:
            if result.stdout:
                output_str += f"STDOUT: {result.stdout}"
            if result.stderr:
                output_str += f"STDERR: {result.stderr}"

        return output_str

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command-line arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)
