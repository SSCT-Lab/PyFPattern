def _get_absolute_path(self, path):
    original_path = path
    if (self._task._role is not None):
        path = self._loader.path_dwim_relative(self._task._role._role_path, 'files', path)
    else:
        path = self._loader.path_dwim_relative(self._loader.get_basedir(), 'files', path)
    if (original_path and (original_path[(- 1)] == '/') and (path[(- 1)] != '/')):
        path += '/'
    return path