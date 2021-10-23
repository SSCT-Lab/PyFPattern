def get_cache_mtime():
    'Return mtime of a valid apt cache file.\n    Stat the apt cache file and if no cache file is found return 0\n    :returns: ``int``\n    '
    cache_time = 0
    if os.path.exists(APT_UPDATE_SUCCESS_STAMP_PATH):
        cache_time = os.stat(APT_UPDATE_SUCCESS_STAMP_PATH).st_mtime
    elif os.path.exists(APT_LISTS_PATH):
        cache_time = os.stat(APT_LISTS_PATH).st_mtime
    return cache_time