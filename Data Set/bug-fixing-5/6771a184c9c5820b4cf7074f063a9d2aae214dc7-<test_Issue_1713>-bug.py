def test_Issue_1713():
    utf32_be = os.path.join(os.path.dirname(__file__), 'test_utf32_be_rcparams.rc')
    old_lang = os.environ.get('LANG', None)
    os.environ['LANG'] = 'en_US.UTF-32-BE'
    rc = mpl.rc_params_from_file(utf32_be, True)
    if old_lang:
        os.environ['LANG'] = old_lang
    else:
        del os.environ['LANG']
    assert (rc.get('timezone') == 'UTC')