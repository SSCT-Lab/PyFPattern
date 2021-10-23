

def find_mount_point(self, path):
    path = os.path.realpath(os.path.expanduser(os.path.expandvars(path)))
    while (not os.path.ismount(path)):
        path = os.path.dirname(path)
    return path
