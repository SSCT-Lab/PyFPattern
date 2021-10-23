def is_plugin_present(plugin_dir, working_dir):
    return os.path.isdir(os.path.join(working_dir, plugin_dir))