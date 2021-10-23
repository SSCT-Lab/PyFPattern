def _load_role_yaml(self, subdir, main=None):
    file_path = os.path.join(self._role_path, subdir)
    if (self._loader.path_exists(file_path) and self._loader.is_directory(file_path)):
        main_file = self._resolve_main(file_path, main)
        if self._loader.path_exists(main_file):
            return self._loader.load_from_file(main_file)
        elif (main is not None):
            raise AnsibleParserError(('Could not find specified file in role: %s' % main))
    return None