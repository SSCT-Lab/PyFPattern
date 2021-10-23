def test_update_on_save():
    pic = novice.Picture(array=np.zeros((3, 3, 3)))
    pic[(0, 0)] = (255, 255, 255)
    with all_warnings():
        pic.size = (6, 6)
    assert pic.modified
    assert (pic.path is None)
    (fd, filename) = tempfile.mkstemp(suffix='.png')
    os.close(fd)
    try:
        pic.save(filename)
        assert (not pic.modified)
        assert_equal(pic.path, os.path.abspath(filename))
        assert_equal(pic.format, 'png')
    finally:
        os.unlink(filename)