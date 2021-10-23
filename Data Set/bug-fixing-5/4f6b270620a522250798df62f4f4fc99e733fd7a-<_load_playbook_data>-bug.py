def _load_playbook_data(self, file_name, variable_manager):
    if os.path.isabs(file_name):
        self._basedir = os.path.dirname(file_name)
    else:
        self._basedir = os.path.normpath(os.path.join(self._basedir, os.path.dirname(file_name)))
    cur_basedir = self._loader.get_basedir()
    self._loader.set_basedir(self._basedir)
    self._file_name = file_name
    for (name, obj) in get_all_plugin_loaders():
        if obj.subdir:
            plugin_path = os.path.join(self._basedir, obj.subdir)
            if os.path.isdir(plugin_path):
                obj.add_directory(plugin_path)
    ds = self._loader.load_from_file(os.path.basename(file_name))
    if (not isinstance(ds, list)):
        self._loader.set_basedir(cur_basedir)
        raise AnsibleParserError('playbooks must be a list of plays', obj=ds)
    for entry in ds:
        if (not isinstance(entry, dict)):
            self._loader.set_basedir(cur_basedir)
            raise AnsibleParserError('playbook entries must be either a valid play or an include statement', obj=entry)
        if (('include' in entry) or ('import_playbook' in entry)):
            if ('include' in entry):
                display.deprecated("You should use 'import_playbook' instead of 'include' for playbook includes")
            pb = PlaybookInclude.load(entry, basedir=self._basedir, variable_manager=variable_manager, loader=self._loader)
            if (pb is not None):
                self._entries.extend(pb._entries)
            else:
                display.display(("skipping playbook include '%s' due to conditional test failure" % entry.get('include', entry)), color=C.COLOR_SKIP)
        else:
            entry_obj = Play.load(entry, variable_manager=variable_manager, loader=self._loader)
            self._entries.append(entry_obj)
    self._loader.set_basedir(cur_basedir)