def pkg_to_dict(pkgstr):
    if pkgstr.strip():
        (n, e, v, r, a, repo) = pkgstr.split('|')
    else:
        return {
            'error_parsing': pkgstr,
        }
    d = {
        'name': n,
        'arch': a,
        'epoch': e,
        'release': r,
        'version': v,
        'repo': repo,
        'envra': ('%s:%s-%s-%s.%s' % (e, n, v, r, a)),
    }
    if (repo == 'installed'):
        d['yumstate'] = 'installed'
    else:
        d['yumstate'] = 'available'
    return d