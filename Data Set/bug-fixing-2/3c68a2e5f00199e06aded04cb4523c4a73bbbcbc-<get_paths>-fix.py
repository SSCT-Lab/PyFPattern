

def get_paths(self, path):
    'Return the list of available content paths under the given path.'
    git = Git(path)
    paths = git.get_file_names(['--cached', '--others', '--exclude-standard'])
    deleted_paths = git.get_file_names(['--deleted'])
    paths = sorted((set(paths) - set(deleted_paths)))
    return paths
