

def parse_setuppy_commands():
    'Check the commands and respond appropriately.  Disable broken commands.\n\n    Return a boolean value for whether or not to run the build or not (avoid\n    parsing Cython and template files if False).\n    '
    if (len(sys.argv) < 2):
        return True
    info_commands = ['--help-commands', '--name', '--version', '-V', '--fullname', '--author', '--author-email', '--maintainer', '--maintainer-email', '--contact', '--contact-email', '--url', '--license', '--description', '--long-description', '--platforms', '--classifiers', '--keywords', '--provides', '--requires', '--obsoletes']
    info_commands.extend(['egg_info', 'install_egg_info', 'rotate'])
    for command in info_commands:
        if (command in sys.argv[1:]):
            return False
    good_commands = ('develop', 'sdist', 'build', 'build_ext', 'build_py', 'build_clib', 'build_scripts', 'bdist_wheel', 'bdist_rpm', 'bdist_wininst', 'bdist_msi', 'bdist_mpkg')
    for command in good_commands:
        if (command in sys.argv[1:]):
            return True
    if ('install' in sys.argv[1:]):
        print(textwrap.dedent('\n            Note: if you need reliable uninstall behavior, then install\n            with pip instead of using `setup.py install`:\n\n              - `pip install .`       (from a git repo or downloaded source\n                                       release)\n              - `pip install numpy`   (last Numpy release on PyPi)\n\n            '))
        return True
    if (('--help' in sys.argv[1:]) or ('-h' in sys.argv[1])):
        print(textwrap.dedent('\n            Numpy-specific help\n            -------------------\n\n            To install Numpy from here with reliable uninstall, we recommend\n            that you use `pip install .`. To install the latest Numpy release\n            from PyPi, use `pip install numpy`.\n\n            For help with build/installation issues, please ask on the\n            numpy-discussion mailing list.  If you are sure that you have run\n            into a bug, please report it at https://github.com/numpy/numpy/issues.\n\n            Setuptools commands help\n            ------------------------\n            '))
        return False
    bad_commands = dict(test='\n            `setup.py test` is not supported.  Use one of the following\n            instead:\n\n              - `python runtests.py`              (to build and test)\n              - `python runtests.py --no-build`   (to test installed numpy)\n              - `>>> numpy.test()`           (run tests for installed numpy\n                                              from within an interpreter)\n            ', upload="\n            `setup.py upload` is not supported, because it's insecure.\n            Instead, build what you want to upload and upload those files\n            with `twine upload -s <filenames>` instead.\n            ", upload_docs='`setup.py upload_docs` is not supported', easy_install='`setup.py easy_install` is not supported', clean="\n            `setup.py clean` is not supported, use one of the following instead:\n\n              - `git clean -xdf` (cleans all files)\n              - `git clean -Xdf` (cleans all versioned files, doesn't touch\n                                  files that aren't checked into the git repo)\n            ", check='`setup.py check` is not supported', register='`setup.py register` is not supported', bdist_dumb='`setup.py bdist_dumb` is not supported', bdist='`setup.py bdist` is not supported', build_sphinx='\n            `setup.py build_sphinx` is not supported, use the\n            Makefile under doc/', flake8='`setup.py flake8` is not supported, use flake8 standalone')
    bad_commands['nosetests'] = bad_commands['test']
    for command in ('upload_docs', 'easy_install', 'bdist', 'bdist_dumb', 'register', 'check', 'install_data', 'install_headers', 'install_lib', 'install_scripts'):
        bad_commands[command] = ('`setup.py %s` is not supported' % command)
    for command in bad_commands.keys():
        if (command in sys.argv[1:]):
            print((textwrap.dedent(bad_commands[command]) + '\nAdd `--force` to your command to use it anyway if you must (unsupported).\n'))
            sys.exit(1)
    import warnings
    warnings.warn('Unrecognized setuptools command, proceeding with generating Cython sources and expanding templates')
    return True
