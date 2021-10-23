def path_dwim_relative(self, path, dirname, source, is_role=False):
    '\n        find one file in either a role or playbook dir with or without\n        explicitly named dirname subdirs\n\n        Used in action plugins and lookups to find supplemental files that\n        could be in either place.\n        '
    search = []
    if (source.startswith('~') or source.startswith(os.path.sep)):
        search.append(self.path_dwim(source))
    else:
        search.append(os.path.join(path, dirname, source))
        basedir = unfrackpath(path)
        if (not is_role):
            is_role = self._is_role(path)
        if (is_role and path.endswith('tasks')):
            basedir = unfrackpath(os.path.dirname(path))
        cur_basedir = self._basedir
        self.set_basedir(basedir)
        search.append(self.path_dwim(os.path.join(basedir, dirname, source)))
        self.set_basedir(cur_basedir)
        if (is_role and (not source.endswith(dirname))):
            search.append(self.path_dwim(os.path.join(basedir, 'tasks', source)))
        search.append(self.path_dwim(os.path.join(dirname, source)))
        search.append(self.path_dwim(os.path.join(basedir, source)))
        search.append(self.path_dwim(source))
    for candidate in search:
        if os.path.exists(to_bytes(candidate, errors='surrogate_or_strict')):
            break
    return candidate