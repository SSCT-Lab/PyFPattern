def _get_columns():
    if (sys.version_info >= (3, 3)):
        (cols, rows) = shutil.get_terminal_size()
        return cols
    return int(os.getenv('COLUMNS', 80))