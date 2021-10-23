def package_split(pkgspec):
    parts = pkgspec.split('=', 1)
    if (len(parts) > 1):
        return (parts[0], parts[1])
    else:
        return (parts[0], None)