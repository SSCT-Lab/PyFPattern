def test_skipper():

    def f():
        pass

    class c():

        def __init__(self):
            self.me = 'I think, therefore...'
    docstring = ' Header\n\n        >>> something # skip if not HAVE_AMODULE\n        >>> something + else\n        >>> a = 1 # skip if not HAVE_BMODULE\n        >>> something2   # skip if HAVE_AMODULE\n        '
    f.__doc__ = docstring
    c.__doc__ = docstring
    global HAVE_AMODULE, HAVE_BMODULE
    HAVE_AMODULE = False
    HAVE_BMODULE = True
    f2 = doctest_skip_parser(f)
    c2 = doctest_skip_parser(c)
    assert_true((f is f2))
    assert_true((c is c2))
    assert_equal(f2.__doc__, ' Header\n\n                 >>> something # doctest: +SKIP\n                 >>> something + else\n                 >>> a = 1\n                 >>> something2\n                 ')
    assert_equal(c2.__doc__, ' Header\n\n                 >>> something # doctest: +SKIP\n                 >>> something + else\n                 >>> a = 1\n                 >>> something2\n                 ')
    HAVE_AMODULE = True
    HAVE_BMODULE = False
    f.__doc__ = docstring
    c.__doc__ = docstring
    f2 = doctest_skip_parser(f)
    c2 = doctest_skip_parser(c)
    assert_true((f is f2))
    assert_equal(f2.__doc__, ' Header\n\n                 >>> something\n                 >>> something + else\n                 >>> a = 1 # doctest: +SKIP\n                 >>> something2   # doctest: +SKIP\n                 ')
    assert_equal(c2.__doc__, ' Header\n\n                 >>> something\n                 >>> something + else\n                 >>> a = 1 # doctest: +SKIP\n                 >>> something2   # doctest: +SKIP\n                 ')
    del HAVE_AMODULE
    f.__doc__ = docstring
    c.__doc__ = docstring
    assert_raises(NameError, doctest_skip_parser, f)
    assert_raises(NameError, doctest_skip_parser, c)