

def setup_package():
    write_version_py()
    cmdclass = {
        'sdist': sdist_checked,
    }
    if HAVE_SPHINX:
        cmdclass['build_sphinx'] = ScipyBuildDoc
    try:
        import numpy
    except ImportError:
        build_requires = ['numpy>=1.13.3']
    else:
        build_requires = (['numpy>=1.13.3'] if ('bdist_wheel' in sys.argv[1:]) else [])
    build_requires += ['pybind11>=2.2.4']
    metadata = dict(name='scipy', maintainer='SciPy Developers', maintainer_email='scipy-dev@python.org', description=DOCLINES[0], long_description='\n'.join(DOCLINES[2:]), url='https://www.scipy.org', download_url='https://github.com/scipy/scipy/releases', project_urls={
        'Bug Tracker': 'https://github.com/scipy/scipy/issues',
        'Documentation': 'https://docs.scipy.org/doc/scipy/reference/',
        'Source Code': 'https://github.com/scipy/scipy',
    }, license='BSD', cmdclass=cmdclass, classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f], platforms=['Windows', 'Linux', 'Solaris', 'Mac OS-X', 'Unix'], test_suite='nose.collector', setup_requires=build_requires, install_requires=build_requires, python_requires='>=3.5')
    if ('--force' in sys.argv):
        run_build = True
        sys.argv.remove('--force')
    else:
        run_build = parse_setuppy_commands()
    os.environ['ACCELERATE'] = 'None'
    from setuptools import setup
    if run_build:
        from numpy.distutils.core import setup
        cmdclass['build_ext'] = get_build_ext_override()
        cwd = os.path.abspath(os.path.dirname(__file__))
        if (not os.path.exists(os.path.join(cwd, 'PKG-INFO'))):
            generate_cython()
        metadata['configuration'] = configuration
    else:
        metadata['version'] = get_version_info()[0]
    setup(**metadata)
