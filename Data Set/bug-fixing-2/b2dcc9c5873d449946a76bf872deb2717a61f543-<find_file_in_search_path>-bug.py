

def find_file_in_search_path(self, myvars, subdir, needle, ignore_missing=False):
    "\n        Return a file (needle) in the task's expected search path.\n        "
    if ('ansible_search_path' in myvars):
        paths = myvars['ansible_search_path']
    else:
        paths = [self.get_basedir(myvars)]
    result = None
    try:
        result = self._loader.path_dwim_relative_stack(paths, subdir, needle)
    except AnsibleFileNotFound:
        if (not ignore_missing):
            self._display.warning(("Unable to find '%s' in expected paths." % needle))
    return result
