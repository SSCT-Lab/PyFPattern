

def _package_dict(self, package):
    'Return a dictionary of information for the package.'
    result = {
        'name': package.name,
        'arch': package.arch,
        'epoch': str(package.epoch),
        'release': package.release,
        'version': package.version,
        'repo': package.repoid,
    }
    result['nevra'] = '{epoch}:{name}-{version}-{release}.{arch}'.format(**result)
    if (package.installtime == 0):
        result['yumstate'] = 'available'
    else:
        result['yumstate'] = 'installed'
    return result
