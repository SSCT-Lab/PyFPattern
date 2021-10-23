

def chown_homedir(self, uid, gid, path):
    try:
        os.chown(path, uid, gid)
        for (root, dirs, files) in os.walk(path):
            for d in dirs:
                os.chown(path, uid, gid)
            for f in files:
                os.chown(os.path.join(root, f), uid, gid)
    except OSError:
        e = get_exception()
        self.module.exit_json(failed=True, msg=('%s' % e))
