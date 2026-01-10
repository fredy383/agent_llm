import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Running a python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File to be runned",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optionnnal properties to add",
            )
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_dir]
        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=abs_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30)

        error_code = result.returncode
        stdout = result.stdout
        stderr = result.stderr
        output = ""
        output2 =""

        if error_code != 0:
            return f"Process exited with code {error_code}"

        if not stdout and not stderr:
            return "No output produced"
        
        if stdout:
            output = f"STDOUT: {stdout}"

        if stderr:
            output2 = f"STDERR: {stderr}"

        return output + output2
    except Exception as e:
        return f"Error : executing Python file: {e}"