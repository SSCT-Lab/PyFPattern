def default_ccache_dir() -> str:
    if ('CCACHE_DIR' in os.environ):
        ccache_dir = os.path.realpath(os.environ['CCACHE_DIR'])
        os.makedirs(ccache_dir, exist_ok=True)
        return ccache_dir
    if (platform.system() == 'Darwin'):
        ccache_dir = '/tmp/_mxnet_ccache'
        os.makedirs(ccache_dir, exist_ok=True)
        return ccache_dir
    return os.path.join(tempfile.gettempdir(), 'ci_ccache')