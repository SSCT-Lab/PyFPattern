

def get_bin_path(self, arg, required=False, opt_dirs=[]):
    '\n        find system executable in PATH.\n        Optional arguments:\n           - required:  if executable is not found and required is true, fail_json\n           - opt_dirs:  optional list of directories to search in addition to PATH\n        if found return full path; otherwise return None\n        '
    sbin_paths = ['/sbin', '/usr/sbin', '/usr/local/sbin']
    paths = []
    for d in opt_dirs:
        if ((d is not None) and os.path.exists(d)):
            paths.append(d)
    paths += os.environ.get('PATH', '').split(os.pathsep)
    bin_path = None
    for p in sbin_paths:
        if ((p not in paths) and os.path.exists(p)):
            paths.append(p)
    for d in paths:
        if (not d):
            continue
        path = os.path.join(d, arg)
        if (os.path.exists(path) and is_executable(path)):
            bin_path = path
            break
    if (required and (bin_path is None)):
        self.fail_json(msg=('Failed to find required executable %s' % arg))
    return bin_path
