def test_Issue_1713():
    utf32_be = os.path.join(os.path.dirname(__file__), 'test_utf32_be_rcparams.rc')
    import locale
    with mock.patch('locale.getpreferredencoding', return_value='UTF-32-BE'):
        rc = mpl.rc_params_from_file(utf32_be, True, False)
    assert (rc.get('timezone') == 'UTC')