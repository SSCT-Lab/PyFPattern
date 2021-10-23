def yum_base(conf_file=None, installroot='/'):
    my = yum.YumBase()
    my.preconf.debuglevel = 0
    my.preconf.errorlevel = 0
    my.preconf.plugins = True
    if (installroot != '/'):
        my.preconf.root = installroot
        my.conf.installroot = installroot
    if (conf_file and os.path.exists(conf_file)):
        my.preconf.fn = conf_file
    if (os.geteuid() != 0):
        if hasattr(my, 'setCacheDir'):
            my.setCacheDir()
        else:
            cachedir = yum.misc.getCacheDir()
            my.repos.setCacheDir(cachedir)
            my.conf.cache = 0
    return my