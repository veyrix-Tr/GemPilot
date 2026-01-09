import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:  
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )
        # Validate that the target directory is within the working directory and Now our LLM agent can't perform any work outside the working_directory that we give it
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files = os.listdir(target_dir)
        file_info=""
        for file in files:
            file_size = os.path.getsize(os.path.join(target_dir, file))
            is_dir = os.path.isdir(os.path.join(target_dir, file))
            file_info += (f"- {file}: file_size={file_size} bytes, is_dir={is_dir}\n")
        return file_info

    except Exception as e:
        return f"Error: {str(e)}"


# We'll be passing "working_directory"from the outside, without the LLM agent knowing about it or being able to affect it
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)