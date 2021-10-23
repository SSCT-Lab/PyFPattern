def all(self, *args, **kwargs):
    ' instantiates all plugins with the same arguments '
    global _PLUGIN_FILTERS
    path_only = kwargs.pop('path_only', False)
    class_only = kwargs.pop('class_only', False)
    all_matches = []
    found_in_cache = True
    for i in self._get_paths():
        all_matches.extend(glob.glob(os.path.join(i, '*.py')))
    for path in sorted(all_matches, key=os.path.basename):
        name = os.path.basename(os.path.splitext(path)[0])
        if (('__init__' in name) or (name in _PLUGIN_FILTERS[self.package])):
            continue
        if path_only:
            (yield path)
            continue
        if (path not in self._module_cache):
            module = self._load_module_source(name, path)
            if (module in self._module_cache.values()):
                continue
            self._module_cache[path] = module
            found_in_cache = False
        try:
            obj = getattr(self._module_cache[path], self.class_name)
        except AttributeError as e:
            display.warning(('Skipping plugin (%s) as it seems to be invalid: %s' % (path, to_text(e))))
            continue
        if self.base_class:
            module = __import__(self.package, fromlist=[self.base_class])
            try:
                plugin_class = getattr(module, self.base_class)
            except AttributeError:
                continue
            if (not issubclass(obj, plugin_class)):
                continue
        self._display_plugin_load(self.class_name, name, self._searched_paths, path, found_in_cache=found_in_cache, class_only=class_only)
        if (not class_only):
            try:
                obj = obj(*args, **kwargs)
            except TypeError as e:
                display.warning(('Skipping plugin (%s) as it seems to be incomplete: %s' % (path, to_text(e))))
        if (not found_in_cache):
            self._load_config_defs(name, path)
        self._update_object(obj, name, path)
        (yield obj)