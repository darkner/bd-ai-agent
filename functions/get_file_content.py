import os
MAX_CHARS = 10_000

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        return f'Error: reading file: {e}'

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Lists file content of a specified file path relative to the working directory, providing file contents as a string",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to list a files content, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}
