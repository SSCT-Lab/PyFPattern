def run(self):
    super(DocCLI, self).run()
    plugin_type = self.options.type
    loader = self.loader_map.get(plugin_type, self.loader_map['module'])
    if self.options.module_path:
        for path in self.options.module_path:
            if path:
                loader.add_directory(path)
    search_paths = DocCLI.print_paths(loader)
    loader._paths = None
    if self.options.list_files:
        paths = loader._get_paths()
        for path in paths:
            self.plugin_list = self.find_plugins(path, plugin_type)
        list_text = self.get_plugin_list_filenames(loader)
        self.pager(list_text)
        return 0
    if self.options.list_dir:
        paths = loader._get_paths()
        for path in paths:
            self.plugin_list = self.find_plugins(path, plugin_type)
        self.pager(self.get_plugin_list_text(loader))
        return 0
    if self.options.all_plugins:
        self.args = self.get_all_plugins_of_type(plugin_type)
    if self.options.json_dump:
        plugin_data = {
            
        }
        for plugin_type in self.loader_map.keys():
            plugin_data[plugin_type] = dict()
            plugin_names = self.get_all_plugins_of_type(plugin_type)
            for plugin_name in plugin_names:
                plugin_data[plugin_type][plugin_name] = self.get_plugin_metadata(plugin_type, plugin_name)
        self.pager(json.dumps(plugin_data, sort_keys=True, indent=4))
        return 0
    if (len(self.args) == 0):
        raise AnsibleOptionsError('Incorrect options passed')
    text = ''
    for plugin in self.args:
        textret = self.format_plugin_doc(plugin, loader, plugin_type, search_paths)
        if textret:
            text += textret
    if text:
        self.pager(text)
    return 0