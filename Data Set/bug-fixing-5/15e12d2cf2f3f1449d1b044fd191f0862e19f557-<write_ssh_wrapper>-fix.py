def write_ssh_wrapper():
    module_dir = get_module_path()
    try:
        if os.access(module_dir, ((os.W_OK | os.R_OK) | os.X_OK)):
            (fd, wrapper_path) = tempfile.mkstemp(prefix=(module_dir + '/'))
        else:
            raise OSError
    except (IOError, OSError):
        (fd, wrapper_path) = tempfile.mkstemp()
    fh = os.fdopen(fd, 'w+b')
    template = b('#!/bin/sh\nif [ -z "$GIT_SSH_OPTS" ]; then\n    BASEOPTS=""\nelse\n    BASEOPTS=$GIT_SSH_OPTS\nfi\n\nif [ -z "$GIT_KEY" ]; then\n    ssh $BASEOPTS "$@"\nelse\n    ssh -i "$GIT_KEY" -o IdentitiesOnly=yes $BASEOPTS "$@"\nfi\n')
    fh.write(template)
    fh.close()
    st = os.stat(wrapper_path)
    os.chmod(wrapper_path, (st.st_mode | stat.S_IEXEC))
    return wrapper_path