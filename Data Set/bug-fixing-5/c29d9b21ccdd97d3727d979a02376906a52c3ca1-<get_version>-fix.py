def get_version(self, package):
    '\n        Get the version of the package from pkg-config.\n        '
    if (not self.has_pkgconfig):
        return None
    (status, output) = subprocess.getstatusoutput((self.pkg_config + (' %s --modversion' % package)))
    if (status == 0):
        return output
    return None