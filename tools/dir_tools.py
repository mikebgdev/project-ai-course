import os


def create_dir(dir_to_create):

    if not os.path.exists(dir_to_create):
        os.makedirs(dir_to_create)

    return dir_to_create + '/'


def check_file_exist(file):
    return os.path.isfile(file)
