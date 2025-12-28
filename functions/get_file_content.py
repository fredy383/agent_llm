import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):

    abs_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_path, file_path))

    # Will be True or False
    valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path

    if not valid_target_dir:
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with open(target_dir, "r") as f:
        file_content_string = f.read(MAX_CHARS)

        if file_content_string:
            # After reading the first MAX_CHARS...
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    
    return file_content_string