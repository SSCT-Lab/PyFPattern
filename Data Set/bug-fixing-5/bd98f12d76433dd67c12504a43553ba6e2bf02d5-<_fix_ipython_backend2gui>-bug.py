@classmethod
@functools.lru_cache()
def _fix_ipython_backend2gui(cls):
    if ('IPython' not in sys.modules):
        return
    import IPython
    ip = IPython.get_ipython()
    if (not ip):
        return
    from IPython.core import pylabtools as pt
    if ((not hasattr(pt, 'backend2gui')) or (not hasattr(ip, 'enable_matplotlib'))):
        return
    backend_mod = sys.modules[cls.__module__]
    rif = getattr(backend_mod, 'required_interactive_framework', None)
    backend2gui_rif = {
        'qt5': 'qt',
        'qt4': 'qt',
        'gtk3': 'gtk3',
        'wx': 'wx',
        'macosx': 'osx',
    }.get(rif)
    if backend2gui_rif:
        pt.backend2gui[get_backend()] = backend2gui_rif
        orig_origbackend = mpl.rcParamsOrig['backend']
        try:
            mpl.rcParamsOrig['backend'] = mpl.rcParams['backend']
            ip.enable_matplotlib()
        finally:
            mpl.rcParamsOrig['backend'] = orig_origbackend