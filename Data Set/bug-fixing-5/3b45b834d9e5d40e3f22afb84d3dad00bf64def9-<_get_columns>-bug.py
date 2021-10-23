def _get_columns():
    try:
        get_terminal_size = shutil.get_terminal_size
    except AttributeError:
        return os.getenv('COLUMNS', 80)
    return get_terminal_size()[0]