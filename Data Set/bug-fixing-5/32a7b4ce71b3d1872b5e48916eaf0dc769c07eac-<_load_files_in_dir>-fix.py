def _load_files_in_dir(self, root_dir, var_files):
    ' Load the found yml files and update/overwrite the dictionary.\n        Args:\n            root_dir (str): The base directory of the list of files that is being passed.\n            var_files: (list): List of files to iterate over and load into a dictionary.\n\n        Returns:\n            Tuple (bool, str, dict)\n        '
    results = dict()
    failed = False
    err_msg = ''
    for filename in var_files:
        stop_iter = False
        if self._task._role:
            if (filename == 'main.yml'):
                stop_iter = True
                continue
        filepath = path.join(root_dir, filename)
        if self.files_matching:
            if (not self.matcher.search(filename)):
                stop_iter = True
        if ((not stop_iter) and (not failed)):
            if (path.exists(filepath) and (not self._ignore_file(filename))):
                (failed, err_msg, loaded_data) = self._load_files(filepath, validate_extensions=True)
                if (not failed):
                    results.update(loaded_data)
    return (failed, err_msg, results)