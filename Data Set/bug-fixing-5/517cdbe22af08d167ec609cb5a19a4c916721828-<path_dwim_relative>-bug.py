def path_dwim_relative(self, path, dirname, source, is_role=False):
    '\n        find one file in either a role or playbook dir with or without\n        explicitly named dirname subdirs\n\n        Used in action plugins and lookups to find supplemental files that\n        could be in either place.\n        '
    search = []
    isrole = False
    if (source.startswith('~') or source.startswith(os.path.sep)):
        search.append(self.path_dwim(source))
    else:
        search.append(os.path.join(path, dirname, source))
        basedir = unfrackpath(path)
        if ((path.endswith('tasks') and os.path.exists(to_bytes(os.path.join(path, 'main.yml'), errors='surrogate_or_strict'))) or os.path.exists(to_bytes(os.path.join(path, 'tasks/main.yml'), errors='surrogate_or_strict'))):
            is_role = True
        if (is_role and path.endswith('tasks')):
            basedir = unfrackpath(os.path.dirname(path))
        cur_basedir = self._basedir
        self.set_basedir(basedir)
        search.append(self.path_dwim(os.path.join(basedir, dirname, source)))
        self.set_basedir(cur_basedir)
        if (isrole and (not source.endswith(dirname))):
            search.append(self.path_dwim(os.path.join(basedir, 'tasks', source)))
        search.append(self.path_dwim(os.path.join(dirname, source)))
        search.append(self.path_dwim(os.path.join(basedir, source)))
        search.append(self.path_dwim(source))
    for candidate in search:
        if os.path.exists(to_bytes(candidate, errors='surrogate_or_strict')):
            break
    return candidate