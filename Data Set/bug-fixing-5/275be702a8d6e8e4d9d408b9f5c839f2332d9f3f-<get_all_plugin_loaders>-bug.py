def get_all_plugin_loaders():
    return [(name, obj) for (name, obj) in inspect.getmembers(sys.modules[__name__]) if isinstance(obj, PluginLoader)]