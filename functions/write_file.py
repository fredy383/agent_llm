import os

def write_file(working_directory, file_path, content):
    
    abs_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_path, file_path))
    parent_dir = os.path.dirname(target_dir)

    # Will be True or False
    valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path

    if not valid_target_dir:
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isdir(target_dir):
        return f'Error: "{file_path}" as it is a directory'
    
    if not os.path.isdir(parent_dir):
        os.makedirs(parent_dir,mode=511,exist_ok=True)
        print("dossier crée")
    
    with open(target_dir, "w") as f:
        f.write(content)
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'