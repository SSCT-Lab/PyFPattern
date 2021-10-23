def _mark_package_install(module, base, pkg_spec):
    'Mark the package for install.'
    try:
        base.install(pkg_spec)
    except dnf.exceptions.MarkingError:
        module.fail_json(msg='No package {0} available.'.format(pkg_spec))