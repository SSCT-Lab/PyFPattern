def get_latest_applicable_version(pypi_data, constraints=None):
    "Get the latest pypi version of the package that we allow\n\n    :arg pypi_data: Pypi information about the data as returned by\n        ``https://pypi.org/pypi/{pkg_name}/json``\n    :kwarg constraints: version constraints on what we're allowed to use as specified by\n        the bundled metadata\n    :returns: The most recent version on pypi that are allowed by ``constraints``\n    "
    latest_version = '0'
    if constraints:
        version_specification = packaging.specifiers.SpecifierSet(constraints)
        for version in pypi_data['releases']:
            if (version in version_specification):
                if (LooseVersion(version) > LooseVersion(latest_version)):
                    latest_version = version
    else:
        latest_version = pypi_data['info']['version']
    return latest_version