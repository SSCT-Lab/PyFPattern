def package_split(pkgspec):
    parts = pkgspec.split('=', 1)
    version = None
    if (len(parts) > 1):
        version = parts[1]
    return (parts[0], version)