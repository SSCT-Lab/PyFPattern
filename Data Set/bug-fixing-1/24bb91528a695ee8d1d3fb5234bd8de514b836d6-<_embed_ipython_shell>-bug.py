

def _embed_ipython_shell(namespace={
    
}, banner=''):
    'Start an IPython Shell'
    try:
        from IPython.terminal.embed import InteractiveShellEmbed
        from IPython.terminal.ipapp import load_default_config
    except ImportError:
        from IPython.frontend.terminal.embed import InteractiveShellEmbed
        from IPython.frontend.terminal.ipapp import load_default_config

    @wraps(_embed_ipython_shell)
    def wrapper(namespace=namespace, banner=''):
        config = load_default_config()
        shell = InteractiveShellEmbed(banner1=banner, user_ns=namespace, config=config)
        shell()
    return wrapper
