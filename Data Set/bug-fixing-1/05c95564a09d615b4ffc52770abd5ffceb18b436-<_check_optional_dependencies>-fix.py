

def _check_optional_dependencies():
    for dep in chainer._version._optional_dependencies:
        name = dep['name']
        pkgs = dep['packages']
        spec = dep['specifier']
        help = dep['help']
        installed = False
        for pkg in pkgs:
            found = False
            requirement = '{}{}'.format(pkg, spec)
            try:
                pkg_resources.require(requirement)
                found = True
            except pkg_resources.DistributionNotFound:
                continue
            except pkg_resources.VersionConflict:
                msg = "\n--------------------------------------------------------------------------------\n{name} ({pkg}) version {version} may not be compatible with this version of Chainer.\nPlease consider installing the supported version by running:\n  $ pip install '{requirement}'\n\nSee the following page for more details:\n  {help}\n--------------------------------------------------------------------------------\n"
                warnings.warn(msg.format(name=name, pkg=pkg, version=pkg_resources.get_distribution(pkg).version, requirement=requirement, help=help))
                found = True
            except Exception:
                warnings.warn('Failed to check requirement: {}'.format(requirement))
                break
            if found:
                if installed:
                    warnings.warn('\n--------------------------------------------------------------------------------\nMultiple installations of {name} package has been detected.\nYou should select only one package from from {pkgs}.\nFollow these steps to resolve this issue:\n  1. `pip list` to list {name} packages installed\n  2. `pip uninstall <package name>` to uninstall all {name} packages\n  3. `pip install <package name>` to install the proper one\n--------------------------------------------------------------------------------\n'.format(name=name, pkgs=pkgs))
                installed = True
