def get_all_plugin_loaders():
    return [(name, obj) for (name, obj) in globals().items() if isinstance(obj, PluginLoader)]