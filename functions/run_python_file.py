import os, subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", abs_file_path]
        if args:
            command.extend(args)
        command_result = subprocess.run(command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30)
        output_string = []
        return_code = command_result.returncode
        stdout = command_result.stdout
        stderr = command_result.stderr
        if return_code != 0:
            output_string.append(f'Process exited with code {return_code}')
        if stdout is None and stderr is None:
            output_string.append(f'No output produced')
        if stdout:
            output_string.append(f'STDOUT: {stdout}')
        if stderr:
            output_string.append(f'STDERR: {stderr}')
        return "\n".join(output_string)
    except Exception as e:
        return f'Error: executing Python file: {e}'


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute Python file with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path of Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "optional arguments to include when executing python file",
                },
            },
            "required": ["file_path"],
        },
    },
}
