


def list_files(folder_path:str) -> list:
    import os
    try:
        return os.listdir(folder_path)
    except filenotfounderror:
        return f"Could not find the folder at {folder_path}"

print(list_files("C:/Users/Eathon/Documents"))