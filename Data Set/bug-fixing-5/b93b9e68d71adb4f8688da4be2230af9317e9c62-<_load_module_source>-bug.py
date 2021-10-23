def _load_module_source(self, name, path):
    if (name in sys.modules):
        return sys.modules[name]
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', RuntimeWarning)
        with open(path, 'rb') as module_file:
            module = imp.load_source(name, path, module_file)
    return module