def close(self):
    ' terminate the connection '
    cache_key = self._cache_key()
    SSH_CONNECTION_CACHE.pop(cache_key, None)
    SFTP_CONNECTION_CACHE.pop(cache_key, None)
    if (self.sftp is not None):
        self.sftp.close()
    if (C.HOST_KEY_CHECKING and C.PARAMIKO_RECORD_HOST_KEYS and self._any_keys_added()):
        lockfile = self.keyfile.replace('known_hosts', '.known_hosts.lock')
        dirname = os.path.dirname(self.keyfile)
        makedirs_safe(dirname)
        KEY_LOCK = open(lockfile, 'w')
        fcntl.lockf(KEY_LOCK, fcntl.LOCK_EX)
        try:
            self.ssh.load_system_host_keys()
            self.ssh._host_keys.update(self.ssh._system_host_keys)
            key_dir = os.path.dirname(self.keyfile)
            if os.path.exists(self.keyfile):
                key_stat = os.stat(self.keyfile)
                mode = key_stat.st_mode
                uid = key_stat.st_uid
                gid = key_stat.st_gid
            else:
                mode = 33188
                uid = os.getuid()
                gid = os.getgid()
            tmp_keyfile = tempfile.NamedTemporaryFile(dir=key_dir, delete=False)
            os.chmod(tmp_keyfile.name, (mode & 4095))
            os.chown(tmp_keyfile.name, uid, gid)
            self._save_ssh_host_keys(tmp_keyfile.name)
            tmp_keyfile.close()
            os.rename(tmp_keyfile.name, self.keyfile)
        except:
            traceback.print_exc()
            pass
        fcntl.lockf(KEY_LOCK, fcntl.LOCK_UN)
    self.ssh.close()