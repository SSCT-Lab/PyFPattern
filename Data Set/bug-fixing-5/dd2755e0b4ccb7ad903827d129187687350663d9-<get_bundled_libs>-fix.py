def get_bundled_libs(paths):
    '\n    Return the set of known bundled libraries\n\n    :arg paths: The paths which the test has been instructed to check\n    :returns: The list of all files which we know to contain bundled libraries.  If a bundled\n        library consists of multiple files, this should be the file which has metadata included.\n    '
    bundled_libs = set()
    for filename in fnmatch.filter(paths, 'lib/ansible/compat/*/__init__.py'):
        bundled_libs.add(filename)
    bundled_libs.add('lib/ansible/module_utils/distro/__init__.py')
    bundled_libs.add('lib/ansible/module_utils/six/__init__.py')
    bundled_libs.add('lib/ansible/module_utils/compat/ipaddress.py')
    bundled_libs.add('lib/ansible/module_utils/urls.py')
    return bundled_libs