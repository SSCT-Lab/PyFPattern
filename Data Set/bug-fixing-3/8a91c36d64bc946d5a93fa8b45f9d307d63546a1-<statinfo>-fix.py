def statinfo(st):
    pw_name = ''
    gr_name = ''
    try:
        pw_name = pwd.getpwuid(st.st_uid).pw_name
    except Exception:
        pass
    try:
        gr_name = grp.getgrgid(st.st_gid).gr_name
    except Exception:
        pass
    return {
        'mode': ('%04o' % stat.S_IMODE(st.st_mode)),
        'isdir': stat.S_ISDIR(st.st_mode),
        'ischr': stat.S_ISCHR(st.st_mode),
        'isblk': stat.S_ISBLK(st.st_mode),
        'isreg': stat.S_ISREG(st.st_mode),
        'isfifo': stat.S_ISFIFO(st.st_mode),
        'islnk': stat.S_ISLNK(st.st_mode),
        'issock': stat.S_ISSOCK(st.st_mode),
        'uid': st.st_uid,
        'gid': st.st_gid,
        'size': st.st_size,
        'inode': st.st_ino,
        'dev': st.st_dev,
        'nlink': st.st_nlink,
        'atime': st.st_atime,
        'mtime': st.st_mtime,
        'ctime': st.st_ctime,
        'gr_name': gr_name,
        'pw_name': pw_name,
        'wusr': bool((st.st_mode & stat.S_IWUSR)),
        'rusr': bool((st.st_mode & stat.S_IRUSR)),
        'xusr': bool((st.st_mode & stat.S_IXUSR)),
        'wgrp': bool((st.st_mode & stat.S_IWGRP)),
        'rgrp': bool((st.st_mode & stat.S_IRGRP)),
        'xgrp': bool((st.st_mode & stat.S_IXGRP)),
        'woth': bool((st.st_mode & stat.S_IWOTH)),
        'roth': bool((st.st_mode & stat.S_IROTH)),
        'xoth': bool((st.st_mode & stat.S_IXOTH)),
        'isuid': bool((st.st_mode & stat.S_ISUID)),
        'isgid': bool((st.st_mode & stat.S_ISGID)),
    }