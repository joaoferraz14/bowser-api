import os


def path_builder(base_path: str, folder: str, file_name: str) -> str:
    return os.path.join(base_path, folder, file_name)
