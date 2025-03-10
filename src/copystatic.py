import os , shutil

def refresh_public(retrieve_dir="./static/", dest_dir="./public/"):
    shutil.rmtree(dest_dir,ignore_errors=True)
    os.mkdir(dest_dir)
    if retrieve_dir[-1] != "/":
                retrieve_dir += "/"
    if dest_dir[-1] != "/":
        dest_dir += "/"
    dir_2_copy = os.listdir(retrieve_dir)
    for file in dir_2_copy:
        if os.path.isdir(retrieve_dir + file):
            ret_sub_dir = f"{retrieve_dir}{file}/"
            dest_sub_dir = f"{dest_dir}{file}/"
            os.mkdir(dest_sub_dir)
            refresh_public(ret_sub_dir, dest_sub_dir)
        else:
            shutil.copy(retrieve_dir + file, dest_dir + file)