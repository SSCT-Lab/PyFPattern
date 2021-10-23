def setup_package():
    metadata = dict(name=DISTNAME, maintainer=MAINTAINER, maintainer_email=MAINTAINER_EMAIL, description=DESCRIPTION, license=LICENSE, url=URL, download_url=DOWNLOAD_URL, version=VERSION, long_description=LONG_DESCRIPTION, classifiers=['Intended Audience :: Science/Research', 'Intended Audience :: Developers', 'License :: OSI Approved', 'Programming Language :: C', 'Programming Language :: Python', 'Topic :: Software Development', 'Topic :: Scientific/Engineering', 'Operating System :: Microsoft :: Windows', 'Operating System :: POSIX', 'Operating System :: Unix', 'Operating System :: MacOS', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 2.7', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.4', 'Programming Language :: Python :: 3.5', 'Programming Language :: Python :: 3.6'], cmdclass=cmdclass, install_requires=['numpy>={0}'.format(NUMPY_MIN_VERSION), 'scipy>={0}'.format(SCIPY_MIN_VERSION)], **extra_setuptools_args)
    if ((len(sys.argv) == 1) or ((len(sys.argv) >= 2) and (('--help' in sys.argv[1:]) or (sys.argv[1] in ('--help-commands', 'egg_info', '--version', 'clean'))))):
        try:
            from setuptools import setup
        except ImportError:
            from distutils.core import setup
        metadata['version'] = VERSION
    else:
        numpy_status = get_numpy_status()
        numpy_req_str = 'scikit-learn requires NumPy >= {0}.\n'.format(NUMPY_MIN_VERSION)
        instructions = 'Installation instructions are available on the scikit-learn website: http://scikit-learn.org/stable/install.html\n'
        if (numpy_status['up_to_date'] is False):
            if numpy_status['version']:
                raise ImportError('Your installation of Numerical Python (NumPy) {0} is out-of-date.\n{1}{2}'.format(numpy_status['version'], numpy_req_str, instructions))
            else:
                raise ImportError('Numerical Python (NumPy) is not installed.\n{0}{1}'.format(numpy_req_str, instructions))
        from numpy.distutils.core import setup
        metadata['configuration'] = configuration
    setup(**metadata)