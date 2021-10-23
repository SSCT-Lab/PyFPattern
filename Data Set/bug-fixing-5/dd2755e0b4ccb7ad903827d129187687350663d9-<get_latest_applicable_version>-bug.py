def get_latest_applicable_version(pypi_data, constraints=None):
    latest_version = '0'
    if ('version_constraints' in metadata):
        version_specification = packaging.specifiers.SpecifierSet(metadata['version_constraints'])
        for version in pypi_data['releases']:
            if (version in version_specification):
                if (LooseVersion(version) > LooseVersion(latest_version)):
                    latest_version = version
    else:
        latest_version = pypi_data['info']['version']
    return latest_version