def file_props(root, path):
    ' Returns dictionary with file properties, or return None on failure '
    abspath = os.path.join(root, path)
    try:
        st = os.lstat(abspath)
    except OSError as e:
        display.warning(('filetree: Error using stat() on path %s (%s)' % (abspath, e)))
        return None
    ret = dict(root=root, path=path)
    if stat.S_ISLNK(st.st_mode):
        ret['state'] = 'link'
        ret['src'] = os.readlink(abspath)
    elif stat.S_ISDIR(st.st_mode):
        ret['state'] = 'directory'
    elif stat.S_ISREG(st.st_mode):
        ret['state'] = 'file'
        ret['src'] = abspath
    else:
        display.warning(('filetree: Error file type of %s is not supported' % abspath))
        return None
    ret['uid'] = st.st_uid
    ret['gid'] = st.st_gid
    try:
        ret['owner'] = pwd.getpwuid(st.st_uid).pw_name
    except KeyError:
        ret['owner'] = st.st_uid
    try:
        ret['group'] = grp.getgrgid(st.st_gid).gr_name
    except KeyError:
        ret['group'] = st.st_gid
    ret['mode'] = ('0%03o' % stat.S_IMODE(st.st_mode))
    ret['size'] = st.st_size
    ret['mtime'] = st.st_mtime
    ret['ctime'] = st.st_ctime
    if (HAVE_SELINUX and (selinux.is_selinux_enabled() == 1)):
        context = selinux_context(abspath)
        ret['seuser'] = context[0]
        ret['serole'] = context[1]
        ret['setype'] = context[2]
        ret['selevel'] = context[3]
    return ret