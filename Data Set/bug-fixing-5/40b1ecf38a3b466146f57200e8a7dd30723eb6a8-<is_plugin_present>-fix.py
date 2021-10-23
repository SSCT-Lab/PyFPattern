def is_plugin_present(plugin_name, plugin_dir):
    return os.path.isdir(os.path.join(plugin_dir, plugin_name))