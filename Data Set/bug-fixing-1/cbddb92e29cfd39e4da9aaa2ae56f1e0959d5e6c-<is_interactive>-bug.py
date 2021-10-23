

def is_interactive():
    return (not hasattr(sys.modules['__main__ '], '__file__'))
