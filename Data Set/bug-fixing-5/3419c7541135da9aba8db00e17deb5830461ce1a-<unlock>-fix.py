def unlock(self):
    '\n        Make sure lock file is available for everyone and Unlock the file descriptor\n        locked by set_lock\n\n        :returns: True\n        '
    if (not self.lockfd):
        return True
    try:
        fcntl.flock(self.lockfd, fcntl.LOCK_UN)
        self.lockfd.close()
    except ValueError:
        pass
    return True