

def skip_if_small_worldsize(func):
    func.skip_if_small_worldsize = True

    @wraps(func)
    def wrapper(*args, **kwargs):
        if ((os.environ['BACKEND'] != 'mpi') and (int(os.environ['WORLD_SIZE']) <= 2)):
            sys.exit(SKIP_IF_SMALL_WORLDSIZE_EXIT_CODE)
        return func(*args, **kwargs)
    return wrapper
