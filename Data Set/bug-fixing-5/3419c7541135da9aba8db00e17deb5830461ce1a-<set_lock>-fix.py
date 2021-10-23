def set_lock(self, path, tmpdir, lock_timeout=None):
    "\n        Create a lock file based on path with flock to prevent other processes\n        using given path.\n        Please note that currently file locking only works when it's executed by\n        the same user, I.E single user scenarios\n\n        :kw path: Path (file) to lock\n        :kw tmpdir: Path where to place the temporary .lock file\n        :kw lock_timeout:\n            Wait n seconds for lock acquisition, fail if timeout is reached.\n            0 = Do not wait, fail if lock cannot be acquired immediately,\n            Default is None, wait indefinitely until lock is released.\n        :returns: True\n        "
    lock_path = os.path.join(tmpdir, 'ansible-{0}.lock'.format(os.path.basename(path)))
    l_wait = 0.1
    r_exception = IOError
    if (sys.version_info[0] == 3):
        r_exception = BlockingIOError
    self.lockfd = open(lock_path, 'w')
    if (lock_timeout <= 0):
        fcntl.flock(self.lockfd, (fcntl.LOCK_EX | fcntl.LOCK_NB))
        os.chmod(lock_path, (stat.S_IWRITE | stat.S_IREAD))
        return True
    if lock_timeout:
        e_secs = 0
        while (e_secs < lock_timeout):
            try:
                fcntl.flock(self.lockfd, (fcntl.LOCK_EX | fcntl.LOCK_NB))
                os.chmod(lock_path, (stat.S_IWRITE | stat.S_IREAD))
                return True
            except r_exception:
                time.sleep(l_wait)
                e_secs += l_wait
                continue
        self.lockfd.close()
        raise LockTimeout('{0} sec'.format(lock_timeout))
    fcntl.flock(self.lockfd, fcntl.LOCK_EX)
    os.chmod(lock_path, (stat.S_IWRITE | stat.S_IREAD))
    return True