

def _check_versions():
    for (modname, minver) in [('cycler', '0.10'), ('dateutil', '2.1'), ('kiwisolver', '1.0.1'), ('numpy', '1.11'), ('pyparsing', '2.0.1')]:
        module = importlib.import_module(modname)
        if (LooseVersion(module.__version__) < minver):
            raise ImportError('Matplotlib requires {}>={}; you have {}'.format(modname, minver, module.__version__))
