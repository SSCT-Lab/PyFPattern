

def run(self):
    super(DocCLI, self).run()
    plugin_type = self.options.type
    if (plugin_type == 'cache'):
        loader = cache_loader
    elif (plugin_type == 'callback'):
        loader = callback_loader
    elif (plugin_type == 'connection'):
        loader = connection_loader
    elif (plugin_type == 'lookup'):
        loader = lookup_loader
    elif (plugin_type == 'strategy'):
        loader = strategy_loader
    elif (plugin_type == 'vars'):
        loader = vars_loader
    elif (plugin_type == 'inventory'):
        loader = PluginLoader('InventoryModule', 'ansible.plugins.inventory', 'inventory_plugins', 'inventory_plugins')
    else:
        loader = module_loader
    if self.options.module_path:
        for path in self.options.module_path:
            if path:
                loader.add_directory(path)
    search_paths = DocCLI.print_paths(loader)
    loader._paths = None
    if self.options.list_dir:
        paths = loader._get_paths()
        for path in paths:
            self.find_plugins(path, plugin_type)
        self.pager(self.get_plugin_list_text(loader))
        return 0
    if self.options.all_plugins:
        paths = loader._get_paths()
        for path in paths:
            self.find_plugins(path, plugin_type)
        self.args = sorted(set(self.plugin_list))
    if (len(self.args) == 0):
        raise AnsibleOptionsError('Incorrect options passed')
    text = ''
    for plugin in self.args:
        try:
            filename = loader.find_plugin(plugin, mod_type='.py', ignore_deprecated=True, check_aliases=True)
            if (filename is None):
                display.warning(('%s %s not found in:\n%s\n' % (plugin_type, plugin, search_paths)))
                continue
            if any((filename.endswith(x) for x in C.BLACKLIST_EXTS)):
                continue
            try:
                (doc, plainexamples, returndocs, metadata) = plugin_docs.get_docstring(filename, verbose=(self.options.verbosity > 0))
            except:
                display.vvv(traceback.format_exc())
                display.error(('%s %s has a documentation error formatting or is missing documentation.' % (plugin_type, plugin)))
                continue
            if (doc is not None):
                doc['plainexamples'] = plainexamples
                doc['returndocs'] = returndocs
                doc['metadata'] = metadata
                if (plugin_type == 'module'):
                    if (plugin in action_loader):
                        doc['action'] = True
                    else:
                        doc['action'] = False
                doc['filename'] = filename
                doc['now_date'] = datetime.date.today().strftime('%Y-%m-%d')
                if ('docuri' in doc):
                    doc['docuri'] = doc[plugin_type].replace('_', '-')
                if (self.options.show_snippet and (plugin_type == 'module')):
                    text += self.get_snippet_text(doc)
                else:
                    text += self.get_man_text(doc)
            else:
                raise AnsibleError('Parsing produced an empty object.')
        except Exception as e:
            display.vvv(traceback.format_exc())
            raise AnsibleError(('%s %s missing documentation (or could not parse documentation): %s\n' % (plugin_type, plugin, str(e))))
    if text:
        self.pager(text)
    return 0
