def _load_module_source(self, name, path):
    full_name = '.'.join([self.package, name])
    if (full_name in sys.modules):
        return sys.modules[full_name]
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', RuntimeWarning)
        with open(path, 'rb') as module_file:
            module = imp.load_source(full_name, path, module_file)
    return module