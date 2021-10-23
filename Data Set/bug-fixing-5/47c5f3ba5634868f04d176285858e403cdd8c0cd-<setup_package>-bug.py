def setup_package():
    src_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)
    write_version_py()
    metadata = dict(name='numpy', maintainer='NumPy Developers', maintainer_email='numpy-discussion@python.org', description=DOCLINES[0], long_description='\n'.join(DOCLINES[2:]), url='http://www.numpy.org', author='Travis E. Oliphant et al.', download_url='http://sourceforge.net/projects/numpy/files/NumPy/', license='BSD', classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f], platforms=['Windows', 'Linux', 'Solaris', 'Mac OS-X', 'Unix'], test_suite='nose.collector', cmdclass={
        'sdist': sdist_checked,
    }, python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*')
    if ('--force' in sys.argv):
        run_build = True
        sys.argv.remove('--force')
    else:
        run_build = parse_setuppy_commands()
    from setuptools import setup
    if run_build:
        from numpy.distutils.core import setup
        cwd = os.path.abspath(os.path.dirname(__file__))
        if (not os.path.exists(os.path.join(cwd, 'PKG-INFO'))):
            generate_cython()
        metadata['configuration'] = configuration
    else:
        metadata['version'] = get_version_info()[0]
    try:
        setup(**metadata)
    finally:
        del sys.path[0]
        os.chdir(old_path)
    return