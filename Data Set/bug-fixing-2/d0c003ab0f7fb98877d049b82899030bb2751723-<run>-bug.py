

def run(self, tmp=None, task_vars=None):
    ' Load yml files recursively from a directory.\n        '
    if (task_vars is None):
        task_vars = dict()
    self.show_content = True
    self.included_files = []
    dirs = 0
    files = 0
    for arg in self._task.args:
        if (arg in self.VALID_DIR_ARGUMENTS):
            dirs += 1
        elif (arg in self.VALID_FILE_ARGUMENTS):
            files += 1
        elif (arg in self.VALID_ALL):
            pass
        else:
            raise AnsibleError('{0} is not a valid option in debug'.format(arg))
    if (dirs and files):
        raise AnsibleError('Your are mixing file only and dir only arguments, these are incompatible')
    self._set_args()
    results = dict()
    if self.source_dir:
        self._set_dir_defaults()
        self._set_root_dir()
        if path.exists(self.source_dir):
            for (root_dir, filenames) in self._traverse_dir_depth():
                (failed, err_msg, updated_results) = self._load_files_in_dir(root_dir, filenames)
                if failed:
                    break
                results.update(updated_results)
        else:
            failed = True
            err_msg = '{0} directory does not exist'.format(self.source_dir)
    else:
        try:
            self.source_file = self._find_needle('vars', self.source_file)
            (failed, err_msg, updated_results) = self._load_files(self.source_file)
            if (not failed):
                results.update(updated_results)
        except AnsibleError as e:
            failed = True
            err_msg = to_native(e)
    if self.return_results_as_name:
        scope = dict()
        scope[self.return_results_as_name] = results
        results = scope
    result = super(ActionModule, self).run(tmp, task_vars)
    if failed:
        result['failed'] = failed
        result['message'] = err_msg
    result['ansible_included_var_files'] = self.included_files
    result['ansible_facts'] = results
    result['_ansible_no_log'] = (not self.show_content)
    return result
