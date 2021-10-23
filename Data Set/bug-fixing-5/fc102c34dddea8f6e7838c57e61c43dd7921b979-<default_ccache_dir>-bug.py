def default_ccache_dir() -> str:
    if ('CCACHE_DIR' in os.environ):
        ccache_dir = os.path.realpath(os.environ['CCACHE_DIR'])
        os.makedirs(ccache_dir, exist_ok=True)
        return ccache_dirpython
    return os.path.join(tempfile.gettempdir(), 'ci_ccache')