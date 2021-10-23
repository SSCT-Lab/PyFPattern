def copytree(src, dst, symlinks=False, ignore=None):
    'like shutil.copytree() but ignores existing files\n    https://stackoverflow.com/a/22331852/1239986\n    '
    if (not os.path.exists(dst)):
        os.makedirs(dst)
        shutil.copystat(src, dst)
    lst = os.listdir(src)
    if ignore:
        excl = ignore(src, lst)
        lst = [x for x in lst if (x not in excl)]
    for item in lst:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if (symlinks and os.path.islink(s)):
            if os.path.lexists(d):
                os.remove(d)
            os.symlink(os.readlink(s), d)
            try:
                st = os.lstat(s)
                mode = stat.S_IMODE(st.st_mode)
                os.lchmod(d, mode)
            except OSError:
                pass
        elif os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)