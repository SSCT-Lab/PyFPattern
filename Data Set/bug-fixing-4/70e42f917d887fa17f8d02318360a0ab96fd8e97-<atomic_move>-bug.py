def atomic_move(self, src, dest, unsafe_writes=False):
    'atomically move src to dest, copying attributes from dest, returns true on success\n        it uses os.rename to ensure this as it is an atomic operation, rest of the function is\n        to work around limitations, corner cases and ensure selinux context is saved if possible'
    context = None
    dest_stat = None
    b_src = to_bytes(src, errors='surrogate_or_strict')
    b_dest = to_bytes(dest, errors='surrogate_or_strict')
    if os.path.exists(b_dest):
        try:
            dest_stat = os.stat(b_dest)
            os.chmod(b_src, (dest_stat.st_mode & PERM_BITS))
            os.chown(b_src, dest_stat.st_uid, dest_stat.st_gid)
            if (hasattr(os, 'chflags') and hasattr(dest_stat, 'st_flags')):
                try:
                    os.chflags(b_src, dest_stat.st_flags)
                except OSError:
                    e = get_exception()
                    for err in ('EOPNOTSUPP', 'ENOTSUP'):
                        if (hasattr(errno, err) and (e.errno == getattr(errno, err))):
                            break
                    else:
                        raise
        except OSError:
            e = get_exception()
            if (e.errno != errno.EPERM):
                raise
        if self.selinux_enabled():
            context = self.selinux_context(dest)
    elif self.selinux_enabled():
        context = self.selinux_default_context(dest)
    creating = (not os.path.exists(b_dest))
    try:
        login_name = os.getlogin()
    except OSError:
        login_name = os.environ.get('LOGNAME', None)
    switched_user = ((login_name and (login_name != pwd.getpwuid(os.getuid())[0])) or os.environ.get('SUDO_USER'))
    try:
        os.rename(b_src, b_dest)
    except (IOError, OSError):
        e = get_exception()
        if (e.errno not in [errno.EPERM, errno.EXDEV, errno.EACCES, errno.ETXTBSY, errno.EBUSY]):
            self.fail_json(msg=('Could not replace file: %s to %s: %s' % (src, dest, e)))
        else:
            b_dest_dir = os.path.dirname(b_dest)
            native_dest_dir = b_dest_dir
            native_suffix = os.path.basename(b_dest)
            native_prefix = b('.ansible_tmp')
            try:
                (tmp_dest_fd, tmp_dest_name) = tempfile.mkstemp(prefix=native_prefix, dir=native_dest_dir, suffix=native_suffix)
            except (OSError, IOError):
                e = get_exception()
                self.fail_json(msg=('The destination directory (%s) is not writable by the current user. Error was: %s' % (os.path.dirname(dest), e)))
            except TypeError:
                self.fail_json(msg='Failed creating temp file for atomic move.  This usually happens when using Python3 less than Python3.5.  Please use Python2.x or Python3.5 or greater.', exception=sys.exc_info())
            b_tmp_dest_name = to_bytes(tmp_dest_name, errors='surrogate_or_strict')
            try:
                try:
                    os.close(tmp_dest_fd)
                    if (switched_user and (os.getuid() != 0)):
                        shutil.copy2(b_src, b_tmp_dest_name)
                    else:
                        shutil.move(b_src, b_tmp_dest_name)
                    if self.selinux_enabled():
                        self.set_context_if_different(b_tmp_dest_name, context, False)
                    try:
                        tmp_stat = os.stat(b_tmp_dest_name)
                        if (dest_stat and ((tmp_stat.st_uid != dest_stat.st_uid) or (tmp_stat.st_gid != dest_stat.st_gid))):
                            os.chown(b_tmp_dest_name, dest_stat.st_uid, dest_stat.st_gid)
                    except OSError:
                        e = get_exception()
                        if (e.errno != errno.EPERM):
                            raise
                    try:
                        os.rename(b_tmp_dest_name, b_dest)
                    except (shutil.Error, OSError, IOError):
                        e = get_exception()
                        if (unsafe_writes and (e.errno == errno.EBUSY)):
                            self._unsafe_writes(b_tmp_dest_name, b_dest)
                        else:
                            self.fail_json(msg=('Unable to rename file: %s to %s: %s' % (src, dest, e)))
                except (shutil.Error, OSError, IOError):
                    e = get_exception()
                    self.fail_json(msg=('Failed to replace file: %s to %s: %s' % (src, dest, e)))
            finally:
                self.cleanup(b_tmp_dest_name)
    if creating:
        umask = os.umask(0)
        os.umask(umask)
        os.chmod(b_dest, (DEFAULT_PERM & (~ umask)))
        if switched_user:
            os.chown(b_dest, os.getuid(), os.getgid())
    if self.selinux_enabled():
        self.set_context_if_different(dest, context, False)