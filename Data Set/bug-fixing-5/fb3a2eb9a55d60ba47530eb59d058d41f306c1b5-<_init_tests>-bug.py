def _init_tests():
    try:
        import faulthandler
    except ImportError:
        pass
    else:
        faulthandler.enable()
    if (not os.path.isdir(os.path.join(os.path.dirname(__file__), 'tests'))):
        raise ImportError('matplotlib test data is not installed')
    LOCAL_FREETYPE_VERSION = '2.6.1'
    from matplotlib import ft2font
    if ((ft2font.__freetype_version__ != LOCAL_FREETYPE_VERSION) or (ft2font.__freetype_build_type__ != 'local')):
        warnings.warn('matplotlib is not built with the correct FreeType version to run tests.  Set local_freetype=True in setup.cfg and rebuild. Expect many image comparison failures below. Expected freetype version {0}. Found freetype version {1}. Freetype build type is {2}local'.format(ft2font.__freetype_version__, LOCAL_FREETYPE_VERSION, ('' if (ft2font.__freetype_build_type__ == 'local') else 'not ')))
    try:
        import nose
        try:
            from unittest import mock
        except:
            import mock
    except ImportError:
        print('matplotlib.test requires nose and mock to run.')
        raise