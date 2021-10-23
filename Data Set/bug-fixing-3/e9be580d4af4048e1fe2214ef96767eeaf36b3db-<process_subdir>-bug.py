def process_subdir(subdir):
    if subdir:
        subdir = subdir.replace('DAGS_FOLDER', settings.DAGS_FOLDER)
        subdir = os.path.abspath(os.path.expanduser(subdir))
        return subdir