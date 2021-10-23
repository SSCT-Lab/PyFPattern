def parse_package_name(names, pkg_spec, module):
    pkg_spec['package_latest_leftovers'] = []
    for name in names:
        module.debug(('parse_package_name(): parsing name: %s' % name))
        version_match = re.search('-[0-9]', name)
        versionless_match = re.search('--', name)
        if (version_match and versionless_match):
            module.fail_json(msg=('package name both has a version and is version-less: ' + name))
        pkg_spec[name] = {
            
        }
        if version_match:
            match = re.search('^(?P<stem>.*)-(?P<version>[0-9][^-]*)(?P<flavor_separator>-)?(?P<flavor>[a-z].*)?$', name)
            if match:
                pkg_spec[name]['stem'] = match.group('stem')
                pkg_spec[name]['version_separator'] = '-'
                pkg_spec[name]['version'] = match.group('version')
                pkg_spec[name]['flavor_separator'] = match.group('flavor_separator')
                pkg_spec[name]['flavor'] = match.group('flavor')
                pkg_spec[name]['style'] = 'version'
            else:
                module.fail_json(msg=('unable to parse package name at version_match: ' + name))
        elif versionless_match:
            match = re.search('^(?P<stem>.*)--(?P<flavor>[a-z].*)?$', name)
            if match:
                pkg_spec[name]['stem'] = match.group('stem')
                pkg_spec[name]['version_separator'] = '-'
                pkg_spec[name]['version'] = None
                pkg_spec[name]['flavor_separator'] = '-'
                pkg_spec[name]['flavor'] = match.group('flavor')
                pkg_spec[name]['style'] = 'versionless'
            else:
                module.fail_json(msg=('unable to parse package name at versionless_match: ' + name))
        else:
            match = re.search('^(?P<stem>.*)$', name)
            if match:
                pkg_spec[name]['stem'] = match.group('stem')
                pkg_spec[name]['version_separator'] = None
                pkg_spec[name]['version'] = None
                pkg_spec[name]['flavor_separator'] = None
                pkg_spec[name]['flavor'] = None
                pkg_spec[name]['style'] = 'stem'
            else:
                module.fail_json(msg=('unable to parse package name at else: ' + name))
        branch_match = re.search('%', pkg_spec[name]['stem'])
        if branch_match:
            branch_release = '6.0'
            if (version_match or versionless_match):
                module.fail_json(msg=("package name using 'branch' syntax also has a version or is version-less: " + name))
            if (StrictVersion(platform.release()) < StrictVersion(branch_release)):
                module.fail_json(msg=("package name using 'branch' syntax requires at least OpenBSD %s: %s" % (branch_release, name)))
            pkg_spec[name]['style'] = 'branch'
            pkg_spec[name]['pkgname'] = pkg_spec[name]['stem'].split('%')[0]
            pkg_spec[name]['branch'] = pkg_spec[name]['stem'].split('%')[1]
        if pkg_spec[name]['flavor']:
            match = re.search('-$', pkg_spec[name]['flavor'])
            if match:
                module.fail_json(msg=('trailing dash in flavor: ' + pkg_spec[name]['flavor']))