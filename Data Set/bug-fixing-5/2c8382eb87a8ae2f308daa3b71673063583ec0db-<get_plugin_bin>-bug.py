def get_plugin_bin(module, plugin_bin):
    if plugin_bin:
        if os.path.isfile(plugin_bin):
            valid_plugin_bin = plugin_bin
        else:
            bin_paths = list(PLUGIN_BIN_PATHS)
            if (plugin_bin and (plugin_bin not in bin_paths)):
                bin_paths.insert(0, plugin_bin)
            plugin_dirs = list(set([os.path.dirname(x) for x in bin_paths]))
            plugin_bins = list(set([os.path.basename(x) for x in bin_paths]))
            for bin_file in plugin_bins:
                valid_plugin_bin = module.get_bin_path(bin_file, opt_dirs=plugin_dirs)
                if valid_plugin_bin:
                    break
    if (not valid_plugin_bin):
        module.fail_json(msg=('%s does not exist and no other valid plugin installers were found. Make sure Elasticsearch is installed.' % plugin_bin))
    return valid_plugin_bin