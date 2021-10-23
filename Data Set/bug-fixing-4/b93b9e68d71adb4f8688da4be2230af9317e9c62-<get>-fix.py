def get(self, name, *args, **kwargs):
    ' instantiates a plugin of the given name using arguments '
    found_in_cache = True
    class_only = kwargs.pop('class_only', False)
    if (name in self.aliases):
        name = self.aliases[name]
    path = self.find_plugin(name)
    if (path is None):
        return None
    if (path not in self._module_cache):
        self._module_cache[path] = self._load_module_source(name, path)
        found_in_cache = False
    obj = getattr(self._module_cache[path], self.class_name)
    if self.base_class:
        module = __import__(self.package, fromlist=[self.base_class])
        try:
            plugin_class = getattr(module, self.base_class)
        except AttributeError:
            return None
        if (not issubclass(obj, plugin_class)):
            return None
    self._display_plugin_load(self.class_name, name, self._searched_paths, path, found_in_cache=found_in_cache, class_only=class_only)
    if (not class_only):
        try:
            obj = obj(*args, **kwargs)
        except TypeError as e:
            if ('abstract' in e.args[0]):
                return None
            raise
    setattr(obj, '_original_path', path)
    setattr(obj, '_load_name', name)
    return obj