def create_homedir(self, path):
    if (not os.path.exists(path)):
        if (self.skeleton is not None):
            skeleton = self.skeleton
        else:
            skeleton = '/etc/skel'
        if os.path.exists(skeleton):
            try:
                shutil.copytree(skeleton, path, symlinks=True)
            except OSError:
                e = get_exception()
                self.module.exit_json(failed=True, msg=('%s' % e))
    else:
        try:
            os.makedirs(path)
        except OSError:
            e = get_exception()
            self.module.exit_json(failed=True, msg=('%s' % e))