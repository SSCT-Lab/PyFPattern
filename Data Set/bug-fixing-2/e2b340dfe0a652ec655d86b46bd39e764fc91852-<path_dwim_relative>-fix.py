

def path_dwim_relative(self, path, dirname, source, is_role=False):
    '\n        find one file in either a role or playbook dir with or without\n        explicitly named dirname subdirs\n\n        Used in action plugins and lookups to find supplemental files that\n        could be in either place.\n        '
    search = []
    source = to_text(source, errors='surrogate_or_strict')
    if (source.startswith(to_text(os.path.sep)) or source.startswith('~')):
        search.append(unfrackpath(source, follow=False))
    else:
        search.append(os.path.join(path, dirname, source))
        basedir = unfrackpath(path, follow=False)
        if (not is_role):
            is_role = self._is_role(path)
        if (is_role and RE_TASKS.search(path)):
            basedir = unfrackpath(os.path.dirname(path), follow=False)
        cur_basedir = self._basedir
        self.set_basedir(basedir)
        search.append(unfrackpath(os.path.join(basedir, dirname, source), follow=False))
        self.set_basedir(cur_basedir)
        if (is_role and (not source.endswith(dirname))):
            search.append(unfrackpath(os.path.join(basedir, 'tasks', source), follow=False))
        search.append(unfrackpath(os.path.join(dirname, source), follow=False))
        search.append(self.path_dwim(os.path.join(dirname, source)))
        search.append(self.path_dwim(source))
    for candidate in search:
        if os.path.exists(to_bytes(candidate, errors='surrogate_or_strict')):
            break
    return candidate
