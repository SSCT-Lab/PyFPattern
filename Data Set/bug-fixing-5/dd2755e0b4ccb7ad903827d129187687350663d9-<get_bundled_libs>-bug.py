def get_bundled_libs(paths):
    bundled_libs = set()
    for filename in fnmatch.filter(paths, 'lib/ansible/compat/*/__init__.py'):
        bundled_libs.add(filename)
    bundled_libs.add('lib/ansible/module_utils/distro/__init__.py')
    bundled_libs.add('lib/ansible/module_utils/six/__init__.py')
    bundled_libs.add('lib/ansible/module_utils/compat/ipaddress.py')
    bundled_libs.add('lib/ansible/module_utils/urls.py')
    return bundled_libs